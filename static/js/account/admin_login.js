import { loginValidationCheck } from "../validation.js";

document.addEventListener("DOMContentLoaded", function () {

    // 管理者ログイン画面のバリデーションチェック
    const emailInput = document.getElementById("floatingInput");
    const passwordInput = document.getElementById("floatingPassword");
    const adminSignInButton = document.getElementById("adminSignInButton");

    loginValidationCheck(emailInput,passwordInput,adminSignInButton);


});


