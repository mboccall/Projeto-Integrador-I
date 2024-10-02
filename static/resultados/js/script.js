function editarCliente(id) {
    // Preencher os campos da div flutuante com os dados do cliente
    var row = document.getElementById("cliente-" + id);
    document.getElementById("edit-id").value = id;
    document.getElementById("edit-nome").value = row.cells[1].textContent;
    document.getElementById("edit-sobrenome").value = row.cells[2].textContent;
    document.getElementById("edit-email").value = row.cells[3].textContent;
    document.getElementById("edit-telefone").value = row.cells[4].textContent;
    document.getElementById("edit-empresa").value = row.cells[5].textContent;
    document.getElementById("edit-checkboxstatus").value = row.cells[6].textContent;
    // Exibir a div flutuante
    document.getElementById("edit-popup").style.display = "block";
}

function fecharPopup() {
    // Fechar a div flutuante
    document.getElementById("edit-popup").style.display = "none";
}

document
    .getElementById("edit-form")
    .addEventListener("submit", function (event) {
        event.preventDefault();
        // Coletar os dados do formulário
        var id = document.getElementById("edit-id").value;
        var nome = document.getElementById("edit-nome").value;
        var sobrenome = document.getElementById("edit-sobrenome").value;
        var email = document.getElementById("edit-email").value;
        var telefone = document.getElementById("edit-telefone").value;
        var empresa = document.getElementById("edit-empresa").value;
        var checkboxstatus = document.getElementById("edit-checkboxstatus").value;

        // Enviar os dados para o servidor via AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", `/editar_cliente/${id}`, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Atualizar a linha da tabela com os novos dados
                    var response = JSON.parse(xhr.responseText);
                    var row = document.getElementById("cliente-" + id);
                    row.cells[1].textContent = response.nome;
                    row.cells[2].textContent = response.sobrenome;
                    row.cells[3].textContent = response.email;
                    row.cells[4].textContent = response.telefone;
                    row.cells[5].textContent = response.empresa;
                    row.cells[6].textContent = response.checkboxstatus;
                    // Fechar a div flutuante
                    fecharPopup();
                } else {
                    alert("Erro ao salvar edição.");
                }
            }
        };
        xhr.send(
            JSON.stringify({
                nome: nome,
                sobrenome: sobrenome,
                email: email,
                telefone: telefone,
                empresa: empresa,
                checkboxstatus: checkboxstatus,
            })
        );
    });

function excluirCliente(id) {
    if (confirm("Tem certeza que deseja excluir este cliente?")) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", `/excluir_cliente/${id}`, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Remover a linha da tabela
                    var row = document.getElementById("cliente-" + id);
                    row.parentNode.removeChild(row);
                } else {
                    alert("Erro ao excluir cliente.");
                }
            }
        };
        xhr.send();
    }
}


// Função para exportar a tabela para um arquivo JSON
document.getElementById('exportButton').addEventListener('click', function () {
  const table = document.querySelector('table tbody');
  const rows = table.querySelectorAll('tr');
  
  // Array para armazenar os dados extraídos
  const data = [];

  // Percorrer as linhas da tabela
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    
    // Criar um objeto para cada linha
    const rowData = {
      ID: cells[0].innerText,
      Nome: cells[1].innerText,
      Sobrenome: cells[2].innerText,
      Email: cells[3].innerText,
      Telefone: cells[4].innerText,
      Empresa: cells[5].innerText,
      Status_do_Checkbox: cells[6].innerText
    };

    data.push(rowData); // Adicionar o objeto ao array de dados
  });

  // Converter os dados para formato JSON
  const json = JSON.stringify(data, null, 2);
  
  // Criar um blob para o JSON e disparar o download
  const blob = new Blob([json], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'dados_tabela.json';
  link.click();
});

// Funções fictícias para edição e exclusão de clientes
function editarCliente(id) {
  alert(`Editar cliente com ID: ${id}`);
}

function excluirCliente(id) {
  alert(`Excluir cliente com ID: ${id}`);
}




