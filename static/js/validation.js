import validator from 'https://cdn.jsdelivr.net/npm/validator@latest/+esm';

// emailのバリデーションチェック
export function emailValidationCheck(emailInput,passwordInput,adminSignInButton) {

    // emailの入力チェック
    emailInput.addEventListener("input", function () {
        let passwordValue = passwordInput.value;
        let emailValue = emailInput.value;

        if (validator.isEmail(emailValue)) {
            emailInput.classList.remove("is-invalid");
        } else {
            emailInput.classList.add("is-invalid");
        }
        if (validator.isEmail(emailValue) && validator.isEmpty(passwordValue)) {
            adminSignInButton.disabled = false;
            adminSignInButton.classList.remove("btn-secondary")
        }else{
            adminSignInButton.disabled = true;
            adminSignInButton.classList.add("btn-secondary")
        }
    });

    // passwordの入力チェック
    passwordInput.addEventListener("input", function () {

        if (validator.isEmail(emailValue) && validator.isEmpty(passwordValue)) {
            adminSignInButton.disabled = false;
            adminSignInButton.classList.remove("btn-secondary")
        }else{
            adminSignInButton.disabled = true;
            adminSignInButton.classList.add("btn-secondary")
        }
    });

}