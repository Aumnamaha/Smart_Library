const API_URL = '/api';

// Theme Toggle Logic
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check for saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    body.classList.add('dark-mode');
    themeToggle.textContent = '☀️';
}

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    themeToggle.textContent = isDark ? '☀️' : '🌙';
});


// UI Navigation
function showSection(sectionId) {
    document.querySelectorAll('section').forEach(s => s.style.display = 'none');
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(sectionId).style.display = 'block';
    document.getElementById(`nav-${sectionId}`).classList.add('active');
    
    if (sectionId === 'booksSection') loadBooks();
    if (sectionId === 'usersSection') loadUsers();
    if (sectionId === 'transactionsSection') loadTransactions();
}

// Modal handling
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Fetch Logic
async function loadBooks() {
    const res = await fetch(`${API_URL}/books/`);
    const books = await res.json();
    const tbody = document.querySelector('#booksTable tbody');
    tbody.innerHTML = '';
    books.forEach(b => {
        tbody.innerHTML += `
            <tr>
                <td>${b.id}</td>
                <td>${b.title}</td>
                <td>${b.author}</td>
                <td>${b.available_copies} / ${b.total_copies}</td>
            </tr>
        `;
    });
}

async function loadUsers() {
    const res = await fetch(`${API_URL}/users/`);
    const users = await res.json();
    const tbody = document.querySelector('#usersTable tbody');
    tbody.innerHTML = '';
    users.forEach(u => {
        tbody.innerHTML += `
            <tr>
                <td>${u.id}</td>
                <td>${u.username}</td>
                <td>${u.is_admin ? 'Admin' : 'User'}</td>
            </tr>
        `;
    });
}

async function loadTransactions() {
    const res = await fetch(`${API_URL}/transactions/`);
    const trans = await res.json();
    const tbody = document.querySelector('#transactionsTable tbody');
    tbody.innerHTML = '';
    trans.forEach(t => {
        const returnAction = t.return_date ? 'Returned' : `<button class="action-btn" onclick="returnBook(${t.id})">Return</button>`;
        tbody.innerHTML += `
            <tr>
                <td>${t.id}</td>
                <td>${t.user_id}</td>
                <td>${t.book_id}</td>
                <td>${t.issue_date}</td>
                <td>${t.return_date || '-'}</td>
                <td>${returnAction}</td>
            </tr>
        `;
    });
}

// Form Submissions
async function addBook(e) {
    e.preventDefault();
    const data = {
        title: document.getElementById('bookTitle').value,
        author: document.getElementById('bookAuthor').value,
        isbn: document.getElementById('bookIsbn').value,
        total_copies: parseInt(document.getElementById('bookCopies').value)
    };
    await fetch(`${API_URL}/books/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    closeModal('bookModal');
    document.getElementById('bookForm').reset();
    loadBooks();
}

async function addUser(e) {
    e.preventDefault();
    const data = {
        username: document.getElementById('userName').value,
        password: document.getElementById('userPass').value,
        is_admin: document.getElementById('userAdmin').checked
    };
    await fetch(`${API_URL}/users/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    closeModal('userModal');
    document.getElementById('userForm').reset();
    loadUsers();
}

async function issueBook(e) {
    e.preventDefault();
    const data = {
        user_id: parseInt(document.getElementById('transUserId').value),
        book_id: parseInt(document.getElementById('transBookId').value)
    };
    
    try {
        const res = await fetch(`${API_URL}/transactions/issue/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const body = await res.json();
            alert(`Error: ${body.detail}`);
            return;
        }
        closeModal('transactionModal');
        document.getElementById('transactionForm').reset();
        loadTransactions();
    } catch(err) {
        console.error(err);
    }
}

async function returnBook(id) {
    try {
        const res = await fetch(`${API_URL}/transactions/return/${id}`, {
            method: 'POST'
        });
        if (!res.ok) {
            const body = await res.json();
            alert(`Error: ${body.detail}`);
            return;
        }
        loadTransactions();
    } catch(err) {
        console.error(err);
    }
}

// Initialize
window.onload = loadBooks;
