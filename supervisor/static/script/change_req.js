function change(btn){
    const btnId = btn.id;
    console.log('Button clicked:', btnId);
    btn.setAttribute('disabled','')
    btn.classList.add('disabled_rule')
    btn.classList.remove('change-btn')
    
    localStorage.setItem(btnId,true);
}

// Add event listeners to buttons
document.querySelectorAll('.change-btn').forEach(btn => {
    btn.addEventListener('click', event => {
        change(event.target);
        alert("Are your Sure .. ? \n You want to Change .. ? \n 🔴Then you can't undo ..!")
    });
});

// Check the state of buttons on page load
window.addEventListener('load', () => {
    document.querySelectorAll('.change-btn').forEach(btn => {
        const btnId = btn.id;
        const isDisabled = localStorage.getItem(btnId);
        if (isDisabled === 'true') {
            btn.setAttribute('disabled', '');
            btn.classList.add('disabled_rule');
            btn.classList.remove('change-btn');
        }
    });
});