import { emailValidationCheck } from "../validation.js";

document.addEventListener("DOMContentLoaded", function () {

    // 管理者ログイン画面のemailのバリデーションチェック
    const emailInput = document.getElementById("floatingInput");
    const passwordInput = document.getElementById("adminSignInButton");
    const adminSignInButton = document.getElementById("adminSignInButton");

    emailValidationCheck(emailInput,passwordInput,adminSignInButton);


});


