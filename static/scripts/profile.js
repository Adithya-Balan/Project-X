const image = document.getElementById('image')
const croppingImg = document.getElementById('croppingImg')
const imgInput = document.getElementById('imgInput')
const cropImgContainer = document.getElementById('cropImgContainer')
const cropBtn = document.getElementById('cropBtn')
const originalProfile = document.getElementById('originalProfile')

let cropper
// for cropping the image
imgInput.addEventListener('change', (event) => {
    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = () => {
            croppingImg.src = reader.result
            cropImgContainer.classList.remove('hidden')
            cropImgContainer.classList.add('flex')

            if (cropper) {
                cropper.destroy()
            }
            cropper = new Cropper(croppingImg, {
                aspectRatio: 1,
                autoCropArea: 1
            })
            cropBtn.classList.remove('hidden')
        }
        reader.readAsDataURL(file)
    }
});

// when crop btn is cliked 
const crop = () => {
    const canvas = cropper.getCroppedCanvas();
    originalProfile.src = canvas.toDataURL()
    image.src = canvas.toDataURL()
    cropImgContainer.classList.add('hidden')
    cropBtn.classList.add('hidden')
}

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


// close edit education function
const closeEditEducation = () => {
    const entireSection = document.getElementById('entireSection')
    const editEducation = document.getElementById('editEducation')
    entireSection.classList.remove('blur-md')
    editEducation.classList.add('hidden')
    editEducation.classList.remove('flex')
    console.log(editEducation)
}

// till now function when the check box is clicked for experience
document.getElementById("presentDate").addEventListener("click", function () {
    if (this.checked) {
        tillNow();
    } else {
        notTillNow();
    }
});

// if check box is clicked
const tillNow = () => {
    document.getElementById('endDate').classList.add('hidden')
    document.getElementById('dateSec').classList.add('items-center')
}

// if check box is not clicked
const notTillNow = () => {
    document.getElementById('endDate').classList.remove('hidden')
    document.getElementById('dateSec').classList.remove('items-center')
}


// till now function when the check box is clicked for education
// document.getElementById("presentDateEducation").addEventListener("click", function () {
//     if (this.checked) {
//         tillNowEducation();
//     } else {
//         notTillNowEducation();
//     }
// });

// if check box is clicked
// const tillNowEducation = () => {
//     document.getElementById('endDateEducation').classList.add('hidden')
//     document.getElementById('dateSecEducation').classList.add('items-center')
// }

// if check box is not clicked
// const notTillNowEducation = () => {
//     document.getElementById('endDateEducation').classList.remove('hidden')
//     document.getElementById('dateSecEducation').classList.remove('items-center')
// }

//only for user-profile.js


