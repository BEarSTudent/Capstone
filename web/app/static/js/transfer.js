const stepTargets = document.querySelectorAll('.step');
const formTargets = document.querySelectorAll('.form');
const stepprev = document.querySelectorAll('.step-status');

const uptp_single_Button = document.querySelector('#singleuploadbtn');
const uptp_double_Button = document.querySelector('#doubleuploadbtn');

let currentStep = 0;

let request_data = {
    user_id : 0,
    person_transfer_bool : 0,
    encoding_type : "",
    content_target_name : "",
    content_target_image : null,
    content_source_name : "",
    content_source_image : null,
    style_name : "",
    style_image : null
}

function stepNext(){
    stepTargets[currentStep].classList.remove('active');
    stepTargets[currentStep].classList.add('prev');
    formTargets[currentStep].classList.add('hidden');

    stepTargets[currentStep + 1].classList.add('active');
    currentStep = currentStep + 1;
}

function stepBack(step){
    stepTargets[currentStep].classList.remove('active');
    currentStep --;

    while(currentStep > step){
        stepTargets[currentStep].classList.remove('prev');
        currentStep --;
    }
    stepTargets[currentStep].classList.remove('prev');
    stepTargets[currentStep].classList.add('active');
    formTargets[currentStep].classList.remove('hidden');
}

window.onload = function(){
    uptp_single_Button.addEventListener('click', ()=>{
        stepNext();
    });
    
    uptp_double_Button.addEventListener('click', ()=>{
        stepNext();
    });
}