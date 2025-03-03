const postBtn = document.getElementById('postBtn')
const projectsBtn = document.getElementById('projectsBtn')
const eventsBtn = document.getElementById('eventsBtn')

const savedProjectSection = document.getElementById('savedProjectSection')
const savedPostSection = document.getElementById('savedPostSection')
const savedEventSection = document.getElementById('savedEventSection')


// for showing the saved post
postBtn.addEventListener('click', () => {
    savedPostSection.classList.remove('hidden')
    savedProjectSection.classList.add('hidden')
    savedEventSection.classList.add('hidden')
})

// for showing the saved projects
projectsBtn.addEventListener('click', () => {
    savedPostSection.classList.add('hidden')
    savedProjectSection.classList.remove('hidden')
    savedEventSection.classList.add('hidden')
})

// for showing the saved events
eventsBtn.addEventListener('click', () => {
    savedPostSection.classList.add('hidden')
    savedProjectSection.classList.add('hidden')
    savedEventSection.classList.remove('hidden')
})

//save.html