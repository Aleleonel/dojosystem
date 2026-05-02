
# 🥋 Dojo System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-Framework-green?logo=django)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> Sistema web profissional para gerenciamento de alunos de artes marciais, com controle de frequência via QR Code e dashboard inteligente.

---

## 📸 Preview do Sistema

> *(adicione prints aqui depois)*



---

## 🚀 Funcionalidades

### 👤 Gestão de Alunos
- Cadastro completo (CRUD)
- Foto do aluno
- Graduação (faixas)
- Status ativo/inativo

---

### 📷 Check-in com QR Code
- QR Code único por aluno
- Leitura via câmera (celular)
- Registro automático de presença

---

### ✅ Controle de Frequência
- Registro manual e automático
- Bloqueio de duplicidade diária
- Histórico individual

---

### 📊 Dashboard Inteligente
- Total de alunos
- Alunos ativos
- Presenças do dia
- Ranking de frequência
- Gráfico de evolução

---

### 📱 Interface Profissional
- Sidebar moderna
- Menu colapsável (mobile)
- Destaque de página ativa
- Layout responsivo

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|----------|------|
| Python | Backend |
| Django | Framework Web |
| SQLite | Banco de dados |
| Bootstrap 5 | UI |
| JavaScript | Interatividade |
| HTML/CSS | Estrutura e estilo |

---

## 📂 Estrutura do Projeto
dojo_system/
│
├── alunos/
├── core/
│
├── templates/
├── static/
│ ├── css/
│ └── js/
│
├── media/
├── manage.py
└── db.sqlite3


---

## ⚙️ Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/dojo_system.git
cd dojo_system

2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate

3. Instale as dependências
pip install -r requirements.txt

4. Migrações
python manage.py makemigrations
python manage.py migrate

5. Criar superusuário
python manage.py createsuperuser

6. Rodar servidor
python manage.py runserver

Acesse:
http://127.0.0.1:8000/

📱 Uso Mobile

O sistema é totalmente utilizável via celular:

📷 Leitor QR direto da câmera
📊 Dashboard responsivo
👨‍🏫 Ideal para uso em aula

🔐 Painel Admin
/admin/

🧠 Roadmap (Próximas Features)
* Sistema de login por professor
* Carteirinha digital do aluno
* Dashboard com filtros por período
* Relatórios em PDF
* Controle financeiro (mensalidades)
* Transformar em PWA (App instalável)

💡 Visão do Projeto

O Dojo System foi pensado para:

Digitalizar academias de artes marciais
Automatizar presença com tecnologia simples
Evoluir para um produto SaaS escalável

🤝 Contribuição

Pull requests são bem-vindos. Para mudanças maiores, abra uma issue primeiro.

📄 Licença

MIT

👨‍💻 Autor

Desenvolvido por Alexandre Leonel de Oliveira

⭐ Apoie o Projeto

Se esse projeto te ajudou:

👉 Deixe uma estrela no repositório
👉 Compartilhe com outros desenvolvedores