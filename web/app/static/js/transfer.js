const stepTargets = document.querySelectorAll('.step');
const formTargets = document.querySelectorAll('.form');
const uploadTargets = document.querySelectorAll('.upload');
const styleTargets = document.querySelectorAll('.style');
const stepprev = document.querySelectorAll('.step-status');
const choose_ex = document.querySelectorAll('.choose');
const choose_back = document.querySelectorAll('.choose_back');
const choose_style = document.querySelectorAll('.choose_style');
const targetName = document.querySelectorAll('.targetname');
const stBox = document.querySelectorAll('.stnoimgbox');

const uptp_single_Button = document.querySelector('#singleuploadbtn');
const uptp_double_Button = document.querySelector('#doubleuploadbtn');
const up_single_Button = document.querySelector('#singlefileupload');
const up_double_Button = document.querySelector('#doublefileupload');
const sttp_s_Button = document.querySelector('#severgiftbtn');
const sttp_d_Button = document.querySelector('#dallebtn');
const sttp_u_Button = document.querySelector('#useruploadbtn');
const st_s_Button = document.querySelector('#stylenorm');
const st_u_Button = document.querySelector('#stylefileupload');
const upload_0 = document.querySelector('#imageone-upload');
const realUpload_0 = document.querySelector('#chooseFile_1');
const upload_1 = document.querySelector('#image-upload_2');
const realUpload_1 = document.querySelector('#chooseFile_2');
const upload_2 = document.querySelector('#image-upload_3');
const realUpload_2 = document.querySelector('#chooseFile_3');
const upload_3 = document.querySelector('#style-upload');
const realUpload_3 = document.querySelector('#chooseFile_4');

let currentStep = 0;
let uploadtype = 0;
let styletype = 0;
let normtype = 0;

let request_data = {
    encoding_type : "",
    content_target_name : "",
    content_target_image : null,
    style_name : "",
    style_image : null,
    person_transfer_bool : false,
    content_source_name : "",
    content_source_image : null
}

function stepNext(){
    stepTargets[currentStep].classList.remove('active');
    stepTargets[currentStep].classList.add('prev');
    formTargets[currentStep].classList.add('hidden');

    stepTargets[currentStep + 1].classList.add('active');
    formTargets[currentStep + 1].classList.remove('hidden');

    if(currentStep == 0){
        uploadTargets[uploadtype].classList.remove('hidden');
    }else{
        uploadTargets[uploadtype].classList.add('hidden');
    }

    if(currentStep == 2){
        styleTargets[styletype].classList.remove('hidden');
    }
    currentStep = currentStep + 1;
}

function hide(){
    uploadTargets[uploadtype].classList.remove('hidden');
    choose_ex[uploadtype].classList.remove('hidden');
    choose_back[0].classList.remove('hidden');
+   document.getElementById('image-show_1').replaceChildren();
    document.getElementById('image-show_2').replaceChildren();
    document.getElementById('image-show_3').replaceChildren();
    targetName[uploadtype].textContent = "example.jpg";
    document.getElementById('fileName_3').textContent = "example.jpg";
    if(currentStep == 0){
        uploadTargets[uploadtype].classList.add('hidden');
    }
}

function stepBack(step){
    stepTargets[currentStep].classList.remove('active');
    formTargets[currentStep].classList.add('hidden');

    if(currentStep ==3){
        styleTargets[styletype].classList.add('hidden');
        if(styletype == 2){
            choose_style[0].classList.remove('hidden');
            document.getElementById('image-show_4').replaceChildren();
            document.getElementById('fileName_4').textContent = "example.jpg";
        }else if(styletype == 0){
            stBox[normtype].classList.remove('select');
        }
    }
    currentStep --;

    while(currentStep > step){
        stepTargets[currentStep].classList.remove('prev');
        formTargets[currentStep].classList.add('hidden');
        currentStep --;
    }
    stepTargets[currentStep].classList.remove('prev');
    stepTargets[currentStep].classList.add('active');
    formTargets[currentStep].classList.remove('hidden');
    if(step <= 1){ 
        hide();
        document.getElementById("check_1").checked = false;
        document.getElementById("check_2").checked = false;
    } else{
        uploadTargets[uploadtype].classList.add('hidden');
    }
}

function select_norm(input){
    stBox[normtype].classList.remove('select');
    stBox[input].classList.add('select');
    normtype = input;

    request_data.style_image = null;
    switch(input){
        case 0 :
            request_data.style_name = "0"
            break;
        case 1 :
            request_data.style_name = "1"
            break; 
        case 2 :
            request_data.style_name = "2"
            break;
        case 3 :
            request_data.style_name = "3"
            break;
        case 4 :
            request_data.style_name = "4"
            break;
        case 5 :
            request_data.style_name = "5"
            break;               
    }
}

function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
    });
}

async function laststep(){
    styleTargets[styletype].classList.add('hidden');

    for(let i =0; i<6; i++){
        stepTargets[i].classList.add('last');
    }

    if(document.getElementById("check_1").checked || document.getElementById("check_2").checked){
        request_data.person_transfer_bool = true;
    } 
    request_data.encoding_type = request_data.content_target_image.type; 
    request_data.content_target_image = await toBase64(request_data.content_target_image);
    request_data.style_image = request_data.style_image ? await toBase64(request_data.style_image) : null;
    request_data.content_source_image =  request_data.content_source_image ? await toBase64( request_data.content_source_image) : null;

    fetch('/sendfile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request_data)
    })
    .then(response => response.json())
    .then(request_data => {
        console.log(request_data);
        // Handle response from Flask here
    })
    .catch(error => {
        console.error('Error:', error);
    });
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
    }else{
        container = document.getElementById('image-show_2');
    }
    
    container.replaceChildren();
    container.appendChild(newImage);
    choose_ex[uploadtype].classList.add('hidden');
}

function loadsource_target(input){
    request_data.content_source_image = input.files[0];
    request_data.content_source_name = request_data.content_source_image.name;

    let name = document.getElementById('fileName_3');
    name.textContent = request_data.content_source_name;

    let newImage = document.createElement("img");

    newImage.src = URL.createObjectURL(request_data.content_source_image);      

    newImage.style.width = "100%";
    newImage.style.height = "100%";
    newImage.style.objectFit = "cover";

    let container = document.getElementById('image-show_3');
    
    container.replaceChildren();
    container.appendChild(newImage);
    choose_back[0].classList.add('hidden');
}

function loadstyle(input){
    request_data.style_image = input.files[0];
    request_data.style_name = request_data.style_image.name;

    let name = document.getElementById('fileName_4');
    name.textContent = request_data.style_name;

    let newImage = document.createElement("img");

    newImage.src = URL.createObjectURL(request_data.style_image);      

    newImage.style.width = "100%";
    newImage.style.height = "100%";
    newImage.style.objectFit = "cover";

    let container = document.getElementById('image-show_4');
    
    container.replaceChildren();
    container.appendChild(newImage);
    choose_style[0].classList.add('hidden');
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

    up_double_Button.addEventListener('click', ()=>{
        stepNext();
    });

    sttp_s_Button.addEventListener('click', ()=>{
        styletype = 0;
        stepNext();
    });

    sttp_d_Button.addEventListener('click', ()=>{
        styletype = 1;
        stepNext();
    });

    sttp_u_Button.addEventListener('click', ()=>{
        styletype = 2;
        stepNext();
    });

    st_s_Button.addEventListener('click', ()=>{
        stepNext();
        laststep();
    });

    st_u_Button.addEventListener('click', ()=>{
        stepNext();
        laststep();
    });

    upload_0.addEventListener('click', () =>{
        realUpload_0.click()
    });

    upload_1.addEventListener('click', () =>{
        realUpload_1.click()
    });

    upload_2.addEventListener('click', () =>{
        realUpload_2.click()
    });

    upload_3.addEventListener('click', () =>{
        realUpload_3.click()
    });

}