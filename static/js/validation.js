import validator from 'https://cdn.jsdelivr.net/npm/validator@latest/+esm';

// emailとpasswordの入力が必要なバリデーションチェック
export function loginValidationCheck(emailInput,passwordInput,adminSignInButton) {

    // emailの入力チェック
    emailInput.addEventListener("blur", function () {
        let passwordValue = passwordInput.value;
        let emailValue = emailInput.value;

        if (validator.isEmail(emailValue)) {
            emailInput.classList.remove("is-invalid");
        } else {
            emailInput.classList.add("is-invalid");
        }
        if (validator.isEmail(emailValue) && !validator.isEmpty(passwordValue)) {
            adminSignInButton.disabled = false;
            adminSignInButton.classList.remove("btn-secondary")
        }else{
            adminSignInButton.disabled = true;
            adminSignInButton.classList.add("btn-secondary")
        }
    });

    // passwordの入力チェック
    passwordInput.addEventListener("blur", function () {
        let passwordValue = passwordInput.value;
        let emailValue = emailInput.value;
        if(!validator.isEmpty(passwordValue)){
            passwordInput.classList.remove("is-invalid");
        }else{
            passwordInput.classList.add("is-invalid");
        }

        if (validator.isEmail(emailValue) && !validator.isEmpty(passwordValue)) {
            adminSignInButton.disabled = false;
            adminSignInButton.classList.remove("btn-secondary")
        }else{
            adminSignInButton.disabled = true;
            adminSignInButton.classList.add("btn-secondary")
        }
    });

}