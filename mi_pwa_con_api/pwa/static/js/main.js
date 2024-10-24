document.addEventListener('DOMContentLoaded', function() {
    const listaPersonas = document.getElementById('personas-list');
    const syncButton = document.getElementById('sync-data');
    const form = document.getElementById('persona-form');

    // Función para obtener la lista de personas desde la API
    async function obtenerPersonas() {
        try {
            const response = await fetch('http://localhost:8000/personas/');
            if (!response.ok) throw new Error('Error en la solicitud.');
            const data = await response.json();
            listaPersonas.innerHTML = ''; // Limpiar la lista antes de agregar nuevas personas
            data.forEach(persona => {
                const li = document.createElement('li');
                li.textContent = `${persona.nombre}, ${persona.edad} años, Tel: ${persona.telefono}`;
                // Botón para eliminar la persona
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Eliminar';
                deleteButton.addEventListener('click', () => eliminarPersona(persona.id));
                li.appendChild(deleteButton);

                // Botón para actualizar la persona (por ejemplo, solo la edad)
                const updateButton = document.createElement('button');
                updateButton.textContent = 'Actualizar Edad';
                updateButton.addEventListener('click', () => actualizarPersona(persona.id, { edad: persona.edad + 1 }));
                li.appendChild(updateButton);

                listaPersonas.appendChild(li);
            });
        } catch (error) {
            console.error('Error al obtener personas:', error);
        }
    }

    // Función para crear una nueva persona
    async function crearPersona(nombre, edad, telefono) {
        try {
            const response = await fetch('http://localhost:8000/personas/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre, edad, telefono })
            });
            if (!response.ok) throw new Error('Error al crear persona.');
            obtenerPersonas(); // Refrescar la lista después de crear la persona
        } catch (error) {
            console.error('Error al crear persona:', error);
        }
    }

    // Función para actualizar una persona
    async function actualizarPersona(id, personaActualizada) {
        try {
            const response = await fetch(`http://localhost:8000/personas/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(personaActualizada)
            });
            if (!response.ok) throw new Error('Error al actualizar persona.');
            obtenerPersonas(); // Refrescar la lista después de actualizar
        } catch (error) {
            console.error('Error al actualizar persona:', error);
        }
    }

    // Función para eliminar una persona
    async function eliminarPersona(id) {
        try {
            const response = await fetch(`http://localhost:8000/personas/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Error al eliminar persona.');
            obtenerPersonas(); // Refrescar la lista después de eliminar
        } catch (error) {
            console.error('Error al eliminar persona:', error);
        }
    }

    // Capturar el formulario para crear una nueva persona
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const nombre = document.getElementById('nombre').value;
        const edad = parseInt(document.getElementById('edad').value, 10);
        const telefono = document.getElementById('telefono').value;

        if (nombre && edad && telefono) {
            crearPersona(nombre, edad, telefono);
            form.reset();  // Limpiar el formulario después de crear la persona
        } else {
            alert('Por favor completa todos los campos');
        }
    });

    // Evento para sincronizar los datos al presionar el botón
    syncButton.addEventListener('click', obtenerPersonas);

    // Obtener la lista de personas al cargar la página
    obtenerPersonas();
});
