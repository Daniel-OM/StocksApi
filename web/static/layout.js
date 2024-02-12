
let dropdowns = document.querySelectorAll('.dropdown-menu')

dropdowns.forEach((dd)=>{

    dd.addEventListener('click', function (e) {
        var el = this.nextElementSibling
        console.log(dd.nextElementSibling);
        console.log(dd);
        dd.style.display = 'block'
    })

})

document.addEventListener('click', (event) => {
    let menu = document.getElementsByClassName('show');
    console.log(event.target);
    console.log(menu);
    if (menu.length > 0 && menu[0].id != event.target.id) {
        for(var i=0;i<menu.length;i++){
            menu[i].classList.remove("show");
            menu[i].style.display = 'none';
        }
    }
})

// let menus = document.querySelectorAll('.dropdown-menu')

// menus.forEach((dd)=>{

//     document.addEventListener("click", (event) => {
//         let menu = document.querySelector('#show');
//         console.log(event.target.id);
//         console.log(menu);
//         if (menu.length > 0) {
//             console.log(menu[0].aria);
//             const isClickInside = menu.contains(event.target);
//             console.log(isClickInside);
//         }
//     });
// })

// let submenus = document.querySelectorAll('.toggle-submenu')

// submenus.forEach((sm)=>{

//     sm.addEventListener('mouseout', function (e) {
//         var el = this.nextElementSibling
//         el.style.display = 'none'
//     })

// })

// let menus = document.querySelectorAll('. .dropdown-menu')

// menus.forEach((menu)=>{

//     menu.addEventListener('mouseout', function (e) {
//         var el = this.nextElementSibling
//         console.log(this);
//         this.style.display = 'none'
//     })

// })