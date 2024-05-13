const nextButton = document.querySelector('#next');
const stepTargets = document.querySelectorAll('.step');
const stepprev = document.querySelectorAll('.step-status');
let currentStep = 0;

nextButton.addEventListener('click', ()=>{
    stepTargets[currentStep].classList.remove('active');
    stepTargets[currentStep].classList.add('prev');

    stepTargets[currentStep + 1].classList.add('active');
    currentStep = currentStep + 1;
});

function stepBack(step){
    stepTargets[currentStep].classList.remove('active');
    currentStep --;

    while(currentStep > step){
        stepTargets[currentStep].classList.remove('prev');
        currentStep --;
    }
    stepTargets[currentStep].classList.remove('prev');
    stepTargets[currentStep].classList.add('active');
}
