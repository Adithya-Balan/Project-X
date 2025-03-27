const image = document.getElementById('image')
const croppingImg = document.getElementById('croppingImg')
const imgInput = document.getElementById('imgInput')
const cropImgContainer = document.getElementById('cropImgContainer')
const cropBtn = document.getElementById('cropBtn')
const originalProfile = document.getElementById('originalProfile')
const croppedImageInput = document.getElementById('croppedImage');

let cropper
// for cropping the image
imgInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            croppingImg.src = reader.result;
            cropImgContainer.classList.remove('hidden');
            cropImgContainer.classList.add('flex');

            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(croppingImg, {
                aspectRatio: 1,
                autoCropArea: 1
            });
            cropBtn.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

// when crop btn is cliked 
const crop = () => {
    if (!cropper) {
        console.error('Cropper instance is not initialized.');
        return;
    }
    const canvas = cropper.getCroppedCanvas();
    if (!canvas) {
        console.error('Failed to get cropped canvas. Ensure the image is loaded and cropped.');
        return;
    }

    const croppedImageData = canvas.toDataURL('image/jpeg'); // Convert to base64 (JPEG format)
    image.src = croppedImageData; // Update the displayed image
    console.log('Updated Image Source:', image.src);

    // Ensure croppedImageInput exists before setting its value
    if (!croppedImageInput) {
        console.error('Hidden input element with id "croppedImage" not found.');
        return;
    }

    croppedImageInput.value = croppedImageData; // Set the hidden input value
    console.log('Hidden Input Value Set:', croppedImageInput.value);

    cropImgContainer.classList.add('hidden');
    cropBtn.classList.add('hidden');
};

// open edit div function
const openEdit = () => {
    const editContainer = document.getElementById('editContainer')
    const entireSection = document.getElementById('entireSection')
    editContainer.classList.remove('hidden')
    editContainer.classList.add('flex')
    entireSection.classList.add('blur-md')
}

// close edit div function
const closeEdit = () => {
    const editContainer = document.getElementById('editContainer')
    const entireSection = document.getElementById('entireSection')
    editContainer.classList.add('hidden')
    editContainer.classList.remove('flex')
    entireSection.classList.remove('blur-md')
}

//open edit current position
const openEditCurrentPosition = () => {
    const entireSection = document.getElementById('entireSection')
    const editCP = document.getElementById('editCurrentPosition')
    entireSection.classList.add('blur-md')
    editCP.classList.remove('hidden')
    editCP.classList.add('flex')
}

const closeCurrentPosition = () => {
    const entireSection = document.getElementById('entireSection')
    const editCP = document.getElementById('editCurrentPosition')
    entireSection.classList.remove('blur-md')
    editCP.classList.add('hidden')
    editCP.classList.remove('flex')
}

// open edit experience function
const openEditExp = () => {
    const entireSection = document.getElementById('entireSection')
    const editExp = document.getElementById('editExp')
    entireSection.classList.add('blur-md')
    editExp.classList.remove('hidden')
    editExp.classList.add('flex')
    console.log(editExp)
}

// close edit experience function
const closeEditExp = () => {
    const entireSection = document.getElementById('entireSection')
    const editExp = document.getElementById('editExp')
    entireSection.classList.remove('blur-md')
    editExp.classList.add('hidden')
    editExp.classList.remove('flex')
    console.log(editExp)
}

//open edit education function
const openEditEducation = () => {
    const entireSection = document.getElementById('entireSection')
    const editEducation = document.getElementById('editEducation')
    entireSection.classList.add('blur-md')
    editEducation.classList.remove('hidden')
    editEducation.classList.add('flex')
    console.log(editEducation)
}

// open edit experience function
const openEditProject = () => {
    const entireSection = document.getElementById('entireSection')
    const editProject = document.getElementById('editProject')
    entireSection.classList.add('blur-md')
    editProject.classList.remove('hidden')
    editProject.classList.add('flex')
    console.log(editProject)
}

// close edit experience function
const closeEditProject = () => {
    const entireSection = document.getElementById('entireSection')
    const editProject = document.getElementById('editProject')
    entireSection.classList.remove('blur-md')
    editProject.classList.add('hidden')
    editProject.classList.remove('flex')
    console.log(editProject)
}


// close edit education function
const closeEditEducation = () => {
    const entireSection = document.getElementById('entireSection')
    const editEducation = document.getElementById('editEducation')
    entireSection.classList.remove('blur-md')
    editEducation.classList.add('hidden')
    editEducation.classList.remove('flex')
    console.log(editEducation)
}

function openAddSkill() {
    const addSkillBtn = document.getElementById('addSkillBtn')
    const addSkillContainer = document.getElementById('addSkillContainer')
    addSkillBtn.classList.toggle('rotate-45')
    addSkillContainer.classList.toggle('hidden')
    addSkillContainer.classList.toggle('flex')
    document.getElementById('skill_list_section').classList.toggle('hidden')
}
