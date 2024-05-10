const nextButton = document.querySelector('#next');
const stepTargets = document.querySelectorAll('.step');
let currentStep = 0;

nextButton.addEventListener('click', ()=>{
    stepTargets[currentStep].classList.remove('active');
    stepTargets[currentStep].classList.add('prev');

    stepTargets[currentStep + 1].classList.add('active');
    currentStep = currentStep + 1;
});