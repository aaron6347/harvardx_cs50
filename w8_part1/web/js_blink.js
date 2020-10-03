function blink()
{
    let body = document.querySelector("body");
    if (body.style.visibility === 'hidden')
    {
        body.style.visibility = "visible";
    }
    else
    {
        body.style.visibility = 'hidden';
    }
}
// what function to fun, how often (ms) should it run
window.setInterval(blink, 500);
