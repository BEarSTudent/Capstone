const stepTargets = document.querySelectorAll('.step');
const formTargets = document.querySelectorAll('.form');
const uploadTargets = document.querySelectorAll('.upload');
const stepprev = document.querySelectorAll('.step-status');
const choose_ex = document.querySelectorAll('.choose');
const targetName = document.querySelectorAll('.targetname');

const uptp_single_Button = document.querySelector('#singleuploadbtn');
const uptp_double_Button = document.querySelector('#doubleuploadbtn');
const up_single_Button = document.querySelector('#singlefileupload');
const upload = document.querySelector('#imageone-upload');
const realUpload = document.querySelector('#chooseFile_1');

let currentStep = 0;
let uploadtype = 0;

let request_data = {
    user_id : 0,
    person_transfer_bool : 1,
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

    if(currentStep == 0){
        uploadTargets[uploadtype].classList.remove('hidden');
    }else{
        uploadTargets[uploadtype].classList.add('hidden');
    }
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
    if(currentStep == 1){
        uploadTargets[uploadtype].classList.remove('hidden');
        choose_ex[uploadtype].classList.remove('hidden');
+       document.getElementById('image-show_1').replaceChildren();
    } else{
        uploadTargets[uploadtype].classList.add('hidden');
    }
}

function loadcontent_target(input){
    request_data.content_target_image = input.files[0];
    request_data.content_target_name = request_data.content_target_image.name;

    let name = targetName[uploadtype];
    name.textContent = request_data.content_target_name;

    let newImage = document.createElement("img");

    newImage.src = URL.createObjectURL(request_data.content_target_image);      

    newImage.style.width = "100%";
    newImage.style.height = "100%";
    newImage.style.objectFit = "cover";

    let container;
    if(uploadtype == 0){
        container = document.getElementById('image-show_1');
    }
    
    container.replaceChildren();
    container.appendChild(newImage);
    choose_ex[uploadtype].classList.add('hidden');
}

window.onload = function(){
    uptp_single_Button.addEventListener('click', ()=>{
        uploadtype = 0;
        stepNext();
    });
    
    uptp_double_Button.addEventListener('click', ()=>{
        uploadtype = 1;
        stepNext();
    });

    up_single_Button.addEventListener('click', ()=>{
        stepNext();
    });

    upload.addEventListener('click', () =>{
        realUpload.click()
    });
}