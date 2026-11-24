/* Salud Mental Joven - interacción en el cliente (E4a, opción 1)
 *  1. Botón "volver arriba"            -> evento scroll + click
 *  2. Selector de idioma automático    -> evento change
 *  3. Filtro de recursos por formato   -> eventos click + efecto de aparición
 *  4. Buscador de artículos            -> AJAX GET (fetch) que devuelve JSON
 *  5. Inscripción en actividades       -> AJAX POST (fetch) con token CSRF
 *  6. Aparición suave de las tarjetas  -> IntersectionObserver
 */
document.addEventListener('DOMContentLoaded', () => {
    iniciarBotonArriba();
    iniciarSelectorIdioma();
    iniciarFiltroRecursos();
    iniciarBuscadorArticulos();
    iniciarInscripcionAjax();
    iniciarAparicionTarjetas();
});

/* 1. Volver arriba */
function iniciarBotonArriba() {
    const boton = document.getElementById('btn-arriba');
    if (!boton) return;
    window.addEventListener('scroll', () => {
        boton.hidden = window.scrollY < 300;
    });
    boton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

/* 2. Al cambiar el idioma se envía el formulario sin pulsar el botón */
function iniciarSelectorIdioma() {
    const form = document.getElementById('lang-form');
    if (!form) return;
    form.querySelector('.lang-btn').hidden = true;
    form.querySelector('select').addEventListener('change', () => form.submit());
}

/* 3. Filtro por formato en la lista de recursos */
function iniciarFiltroRecursos() {
    const botones = document.querySelectorAll('.filtro');
    const recursos = document.querySelectorAll('.recurso');
    botones.forEach((boton) => {
        boton.addEventListener('click', () => {
            botones.forEach((b) => b.classList.remove('activo'));
            boton.classList.add('activo');
            const formato = boton.dataset.formato;
            recursos.forEach((r) => {
                const visible = formato === 'todos' || r.dataset.formato === formato;
                r.hidden = !visible;
                if (visible) {
                    r.classList.remove('aparecer');
                    void r.offsetWidth; // reinicia la animación CSS
                    r.classList.add('aparecer');
                }
            });
        });
    });
}

/* 4. Buscador AJAX: pide JSON al servidor y pinta las tarjetas */
function iniciarBuscadorArticulos() {
    const input = document.getElementById('buscador-articulos');
    if (!input) return;
    const lista = document.getElementById('lista-articulos');
    const estado = document.getElementById('buscador-estado');
    // Textos traducidos que vienen de la plantilla en atributos data-*
    const textos = { leer: input.dataset.textoLeer, vacio: input.dataset.textoVacio, resultados: input.dataset.textoResultados };
    let temporizador;

    input.addEventListener('input', () => {
        clearTimeout(temporizador);
        // "debounce": esperamos 300 ms desde la última tecla antes de llamar al servidor
        temporizador = setTimeout(async () => {
            const url = `${input.dataset.url}?q=${encodeURIComponent(input.value)}`;
            try {
                const respuesta = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
                if (!respuesta.ok) throw new Error(respuesta.status);
                const datos = await respuesta.json();
                pintarArticulos(lista, datos.articulos, textos);
                estado.textContent = datos.consulta ? `${datos.total} ${textos.resultados}` : '';
            } catch (error) {
                estado.textContent = '⚠ Error';
            }
        }, 300);
    });
}

function pintarArticulos(lista, articulos, textos) {
    lista.replaceChildren();
    if (articulos.length === 0) {
        const p = document.createElement('p');
        p.textContent = textos.vacio;
        lista.append(p);
        return;
    }
    articulos.forEach((a) => {
        // textContent (y no innerHTML) para evitar inyección de HTML (XSS)
        const card = document.createElement('article');
        card.className = 'info-card aparecer';
        const cat = document.createElement('span');
        cat.className = 'card-number';
        cat.textContent = a.categorias.join(' · ').toUpperCase();
        const h2 = document.createElement('h2');
        h2.textContent = a.titulo;
        const p = document.createElement('p');
        p.textContent = a.resumen;
        const enlace = document.createElement('a');
        enlace.className = 'tag';
        enlace.href = a.url;
        enlace.textContent = `${textos.leer} →`;
        card.append(cat, h2, p, enlace);
        lista.append(card);
    });
}

/* 5. Inscripción AJAX: envía el formulario sin recargar la página */
function iniciarInscripcionAjax() {
    const form = document.getElementById('form-inscripcion');
    if (!form) return;
    const resultado = document.getElementById('inscripcion-resultado');
    const plazas = document.getElementById('plazas-libres');

    form.addEventListener('submit', async (evento) => {
        evento.preventDefault();
        form.querySelectorAll('.campo-error').forEach((s) => { s.textContent = ''; });
        resultado.textContent = '';
        resultado.className = 'form-resultado';

        try {
            const respuesta = await fetch(window.location.href, {
                method: 'POST',
                body: new FormData(form), // incluye csrfmiddlewaretoken
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            });
            const datos = await respuesta.json();
            if (datos.ok) {
                resultado.textContent = datos.mensaje;
                resultado.classList.add('alert', 'alert-success', 'aparecer');
                plazas.textContent = datos.plazas_libres;
                form.reset();
                if (datos.plazas_libres === 0) form.hidden = true;
            } else {
                Object.entries(datos.errores).forEach(([campo, errores]) => {
                    const texto = errores.map((e) => e.message).join(' ');
                    const span = document.getElementById(`error-${campo}`);
                    if (span) {
                        span.textContent = texto;
                    } else {
                        resultado.textContent = texto; // errores generales (__all__)
                        resultado.classList.add('alert', 'alert-error', 'aparecer');
                    }
                });
            }
        } catch (error) {
            form.submit(); // si falla AJAX, se envía de forma normal
        }
    });
}

/* 6. Las tarjetas aparecen suavemente al entrar en pantalla */
function iniciarAparicionTarjetas() {
    if (!('IntersectionObserver' in window)) return;
    const observador = new IntersectionObserver((entradas) => {
        entradas.forEach((entrada) => {
            if (entrada.isIntersecting) {
                entrada.target.classList.add('aparecer');
                observador.unobserve(entrada.target);
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.cards-grid .info-card').forEach((card) => observador.observe(card));
}
