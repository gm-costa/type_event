const inputSenha = document.querySelector('input[name=senha]');
const inputConfSenha = document.querySelector('input[name=confirmar_senha]');
const spans = document.querySelectorAll('span');
const spanSenha = spans[0];
const spanConfSenha = spans[1];
const divBar = document.querySelector('div[class~=progress-stacked]');
const divsInternasBar = document.querySelectorAll('div[class~=progress-bar]');

divBar.style.display = 'none';
inputSenha.addEventListener('input', forcaSenha);
inputConfSenha.addEventListener('input', confereSenha);

function forcaSenha() {

    let senha = inputSenha.value;
    const t_senha = senha.length;
    
    spanSenha.removeAttribute('class');
    spanConfSenha.removeAttribute('class');

    if(senha) {

        let minusculas =senha.match(/[a-z]+/);
        let maiusculas =senha.match(/[A-Z]+/);
        let numeros =senha.match(/\d+/);
        let char_especial =senha.match(/\W+/);

        const s_fraca = (t_senha < 8) || minusculas || maiusculas || numeros;
        
        const s_media = (t_senha >= 8) && ((minusculas && numeros) || (maiusculas && numeros));
        
        const s_boa = (t_senha >= 8) && ((minusculas && numeros && maiusculas) || (minusculas && numeros && char_especial) || (maiusculas && numeros && char_especial));
        
        const s_forte = (t_senha >= 8) &&  (minusculas && maiusculas && numeros && char_especial);     

        if(s_forte) {
            spanSenha.textContent = 'forte';
            spanSenha.setAttribute('class', 'text-success ms-2');
            for(let i=0; i<4; i++) {
                divsInternasBar[i].classList.remove('bg-transparent');
            }
        } else if(s_boa) {
            spanSenha.textContent = 'boa';
            spanSenha.setAttribute('class', 'text-primary ms-2');
            divsInternasBar[1].classList.remove('bg-transparent');
            divsInternasBar[2].classList.remove('bg-transparent');
            divsInternasBar[3].classList.add('bg-transparent');
        } else if(s_media) {
            spanSenha.textContent = 'media';
            spanSenha.setAttribute('class', 'text-warning ms-2');
            divsInternasBar[1].classList.remove('bg-transparent');
            divsInternasBar[2].classList.add('bg-transparent');
            divsInternasBar[3].classList.add('bg-transparent');
        } else if(s_fraca) {
            spanSenha.textContent = 'fraca';
            spanSenha.setAttribute('class', 'text-danger ms-2');
            divsInternasBar[0].classList.remove('bg-transparent');
            divsInternasBar[1].classList.add('bg-transparent');
            divsInternasBar[2].classList.add('bg-transparent');
            divsInternasBar[3].classList.add('bg-transparent');
        }
        
        divBar.style.display = 'flex';

    } else {
        spanSenha.textContent = '';
        divBar.style.display = 'none';
    }
}

function confereSenha() {

    if(inputConfSenha.value) {

        if(inputSenha.value === inputConfSenha.value) {
            // spanConfSenha.textContent = '<i class="bi bi-hand-thumbs-up-fill text-success"></i>';
            spanConfSenha.innerHTML = '<i class="bi bi-hand-thumbs-up-fill text-success"></i>';
            spanConfSenha.setAttribute('class', 'text-success ms-2');
        } else {
            // spanConfSenha.textContent = '<i class="bi bi-hand-thumbs-down-fill text-danger"></i>';
            spanConfSenha.innerHTML = '<i class="bi bi-hand-thumbs-down-fill text-danger"></i>';
            spanConfSenha.setAttribute('class', 'text-danger ms-2');
        }
    
    } else {
        // spanConfSenha.textContent = '';
        spanConfSenha.innerHTML = '';
    }
}