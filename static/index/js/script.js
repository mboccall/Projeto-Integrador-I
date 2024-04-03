document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("cadastroForm");
  const telefoneInput = document.getElementById("celular");

  const iti = window.intlTelInput(telefoneInput, {
    initialCountry: "br",
    preferredCountries: ["br"],
    utilsScript:
      "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
  });

  form.addEventListener("submit", function (event) {
    let valid = true;

    // Validação do telefone
    if (!iti.isValidNumber()) {
      valid = false;
      document.querySelector("#celular + .error-message").innerText =
        "Insira um número de telefone válido";
      event.preventDefault();
    } else {
      document.querySelector("#celular + .error-message").innerText = "";
    }

    return valid;
  });
});