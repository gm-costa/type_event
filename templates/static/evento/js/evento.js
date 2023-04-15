const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const btnRemFiltro = document.getElementById('btnRemoveFiltro');
const inputNome = document.querySelector('input[name=nome]');
const inputData = document.querySelector('input[name=data]');
const inputStatus = document.querySelector('select[name=status]');
const btnFiltar = document.querySelector('input[type=submit]');

btnRemFiltro.addEventListener('click', (e) => {

    e.preventDefault();

    inputNome.value = "";
    inputData.value = "";
    inputStatus.value = "";
    btnFiltar.click();

});
