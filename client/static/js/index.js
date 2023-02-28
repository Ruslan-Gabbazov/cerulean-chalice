path = '${CONNECT_PATH}';
init()

document.getElementById('enter').addEventListener('click', listener);

function listener() {

    const loginInput = document.querySelector("[name=login]");
    const passwordInput = document.querySelector("[name=password]");
    const checkboxButton = document.querySelector("[name=register]");

    if (checkboxButton.checked) {
        signUp(loginInput.value, passwordInput.value);
    } else {
        signIn(loginInput.value, passwordInput.value);
    }
}
