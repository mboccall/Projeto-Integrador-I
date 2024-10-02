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


// Função para extrair os dados da tabela e salvar como JSON
document.getElementById('exportButton').addEventListener('click', function () {
    let tableData = [];
    const tableRows = document.querySelectorAll('tbody tr');

    tableRows.forEach(row => {
        const rowData = {
            ID: row.cells[0].textContent.trim(),
            Nome: row.cells[1].textContent.trim(),
            Sobrenome: row.cells[2].textContent.trim(),
            Email: row.cells[3].textContent.trim(),
            Telefone: row.cells[4].textContent.trim(),
            Empresa: row.cells[5].textContent.trim(),
            Status: row.cells[6].textContent.trim()
        };
        tableData.push(rowData);
    });

    // Cria o JSON stringificado
    const json = JSON.stringify(tableData, null, 2);

    // Cria um Blob com os dados JSON
    const blob = new Blob([json], { type: 'application/json' });

    // Cria um link temporário para download
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'dados_tabela.json';

    // Adiciona o link ao documento e clica nele para download
    document.body.appendChild(link);
    link.click();

    // Remove o link temporário do documento
    document.body.removeChild(link);
});

// Funções fictícias para editar e excluir (para manter o HTML funcional)
function editarCliente(id) {
    alert('Editar cliente com ID: ' + id);
}

function excluirCliente(id) {
    alert('Excluir cliente com ID: ' + id);
}
 
