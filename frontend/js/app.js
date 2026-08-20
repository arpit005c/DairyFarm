"use strict";

document.addEventListener("DOMContentLoaded", () => {
    // -----------------------------------------
    // SPA Navigation & UI State
    // -----------------------------------------
    const navLinks = document.querySelectorAll('.nav-spa .nav-link');
    const viewSections = document.querySelectorAll('.view-section');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }

    function switchView(targetViewId) {
        viewSections.forEach(section => {
            if (section.id === targetViewId) {
                section.classList.remove('d-none');
                section.classList.add('active');
            } else {
                section.classList.add('d-none');
                section.classList.remove('active');
            }
        });

        navLinks.forEach(link => {
            if (link.getAttribute('data-view') === targetViewId) {
                link.classList.add('active');
                link.classList.remove('link-dark');
            } else {
                link.classList.remove('active');
                link.classList.add('link-dark');
            }
        });

        // Load data based on view
        if (targetViewId === 'dashboard-view') { if (window.loadAnalytics) window.loadAnalytics(); }
        if (targetViewId === 'farmers-view') loadFarmers();
        if (targetViewId === 'cattle-view') loadCattle();
        if (targetViewId === 'milk-view') loadMilkRecords();
        if (targetViewId === 'feed-view') loadFeedRecords();
        if (targetViewId === 'expenses-view') loadExpenses();
        if (targetViewId === 'revenue-view') loadRevenue();
        
        if (window.innerWidth <= 768 && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetView = link.getAttribute('data-view');
            switchView(targetView);
            window.location.hash = targetView.replace('-view', '');
        });
    });

    // Handle initial load based on hash
    const hash = window.location.hash;
    if (hash) {
        const viewId = hash.substring(1) + '-view';
        if (document.getElementById(viewId)) {
            switchView(viewId);
        } else {
            switchView('dashboard-view');
        }
    } else {
        switchView('dashboard-view');
    }

    // -----------------------------------------
    // Toast Notification System
    // -----------------------------------------
    function showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const id = 'toast-' + Date.now();
        let icon = type === 'success' ? 'bi-check-circle-fill text-success' : 'bi-exclamation-triangle-fill text-danger';
        
        const toastHTML = `
            <div id="${id}" class="toast align-items-center border-0 shadow" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body d-flex align-items-center">
                        <i class="bi ${icon} me-2 fs-5"></i>
                        <span>${message}</span>
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', toastHTML);
        const toastElement = document.getElementById(id);
        const bsToast = new bootstrap.Toast(toastElement, { delay: 4000 });
        bsToast.show();
        
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    // -----------------------------------------
    // Formatting Utilities
    // -----------------------------------------
    const formatCurrency = (val) => '₹' + parseFloat(val).toLocaleString('en-IN', { minimumFractionDigits: 2 });
    const formatNumber = (val) => parseFloat(val).toLocaleString('en-IN');
    
    // Chart instances
    let milkChartInstance = null;
    let financeChartInstance = null;

    // -----------------------------------------
    // Data Loading Functions
    // -----------------------------------------
    window.loadAnalytics = async function() {
        try {
            const response = await fetch('http://localhost:8000/api/analytics');
            if (!response.ok) throw new Error('Failed to load analytics');
            const data = await response.json();
            const summary = data.summary;
            const detailed = data.detailed;

            // Overview Data
            document.getElementById('kpi-milk').innerText = `${data.summary.milk_production.total_production.toFixed(1)} L`;
            
            const totalRevenue = formatCurrency(data.summary.revenue.total_revenue || 0);
            const totalExpenses = formatCurrency(data.summary.expenses.total_expense || 0);
            
            document.getElementById('kpi-revenue').innerText = totalRevenue;
            document.getElementById('kpi-expenses').innerText = totalExpenses;
            
            document.getElementById('kpi-profit').textContent = formatCurrency(summary.financial_summary.net_profit);

            // Update Milk Chart
            const milkCtx = document.getElementById('milkChart');
            if (milkCtx && detailed.milk_production_time_series) {
                const milkData = detailed.milk_production_time_series;
                const labels = Object.keys(milkData);
                const values = Object.values(milkData);

                if (milkChartInstance) milkChartInstance.destroy();
                milkChartInstance = new Chart(milkCtx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Milk Production (L)',
                            data: values,
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }

            // Update Finance Chart
            const finCtx = document.getElementById('financeChart');
            if (finCtx) {
                if (financeChartInstance) financeChartInstance.destroy();
                financeChartInstance = new Chart(finCtx, {
                    type: 'bar',
                    data: {
                        labels: ['Revenue', 'Expenses', 'Profit'],
                        datasets: [{
                            data: [
                                summary.financial_summary.total_revenue, 
                                summary.financial_summary.total_expenses, 
                                Math.max(0, summary.financial_summary.net_profit)
                            ],
                            backgroundColor: ['#10b981', '#ef4444', '#3b82f6'],
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }
        } catch (err) {
            console.error("Analytics load error:", err);
            // Don't toast on initial load failure to avoid spam if backend is starting
        }
    };

    async function loadTableData(url, tableBodyId, renderRowFn, emptyCols) {
        const tbody = document.querySelector(`#${tableBodyId} tbody`);
        try {
            tbody.innerHTML = `<tr><td colspan="${emptyCols}" class="text-center py-5 text-muted"><div class="spinner-border spinner-border-sm me-2" role="status"></div> Loading...</td></tr>`;
            const response = await fetch(`http://localhost:8000${url}`);
            if (!response.ok) throw new Error('Failed to load data');
            const json = await response.json();
            const data = json.data || [];
            
            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="${emptyCols}" class="text-center py-5 text-muted">No records found.</td></tr>`;
            } else {
                tbody.innerHTML = data.map(renderRowFn).join('');
            }
        } catch (err) {
            tbody.innerHTML = `<tr><td colspan="${emptyCols}" class="text-center py-5 text-danger">Error loading data.</td></tr>`;
        }
    }

    function loadFarmers() {
        loadTableData('/api/farmers', 'farmers-table', f => `
            <tr>
                <td class="ps-4 fw-bold text-muted">#${f.farmer_id}</td>
                <td class="fw-bold">${f.full_name}</td>
                <td>${f.phone}</td>
                <td>${f.email || '-'}</td>
                <td>${f.address || '-'}</td>
            </tr>
        `, 5);
    }

    function loadCattle() {
        loadTableData('/api/cattle', 'cattle-table', c => `
            <tr>
                <td class="ps-4 fw-bold text-muted">#${c.cattle_id}</td>
                <td class="fw-bold"><span class="badge bg-light text-dark border">${c.tag_number}</span></td>
                <td>${c.name || '-'}</td>
                <td>${c.breed || '-'}</td>
                <td class="text-capitalize">${c.gender}</td>
                <td><span class="badge ${c.status === 'active' ? 'bg-success' : 'bg-secondary'}">${c.status}</span></td>
                <td>#${c.farmer_id}</td>
            </tr>
        `, 7);
    }

    function loadMilkRecords() {
        loadTableData('/api/milk-records', 'milk-table', m => `
            <tr>
                <td class="ps-4 fw-bold text-muted">#${m.milk_record_id}</td>
                <td>${m.record_date}</td>
                <td class="text-capitalize">${m.session}</td>
                <td class="fw-bold text-primary">${m.quantity_litres} L</td>
                <td>#${m.cattle_id}</td>
            </tr>
        `, 5);
    }

    function loadFeedRecords() {
        loadTableData('/api/feed-records', 'feed-table', f => `
            <tr>
                <td class="ps-4 fw-bold text-muted">#${f.feed_record_id}</td>
                <td>${f.record_date}</td>
                <td>${f.feed_type}</td>
                <td class="fw-bold">${f.quantity_kg} kg</td>
                <td class="text-danger fw-bold">${formatCurrency(f.cost)}</td>
                <td>#${f.cattle_id || '-'}</td>
            </tr>
        `, 6);
    }

    function loadExpenses() {
        loadTableData('/api/expenses', 'expenses-table', e => `
            <tr>
                <td class="ps-4 fw-bold text-muted">#${e.expense_id}</td>
                <td>${e.expense_date}</td>
                <td><span class="badge bg-light text-dark border">${e.category}</span></td>
                <td class="text-danger fw-bold">${formatCurrency(e.amount)}</td>
                <td class="text-truncate" style="max-width: 200px;" title="${e.description}">${e.description}</td>
            </tr>
        `, 5);
    }

    function loadRevenue() {
        loadTableData('/api/revenue', 'revenue-table', r => `
            <tr>
                <td class="ps-4 fw-bold text-muted">#${r.revenue_id}</td>
                <td>${r.sale_date}</td>
                <td class="fw-bold">${r.quantity_litres} L</td>
                <td>${formatCurrency(r.price_per_litre)}</td>
                <td>${r.buyer_name}</td>
                <td class="text-success fw-bold">${formatCurrency(r.amount || (r.quantity_litres * r.price_per_litre))}</td>
            </tr>
        `, 6);
    }

    // -----------------------------------------
    // Form Submission & Validation Helpers
    // -----------------------------------------
    function isValidName(val) { return /^[A-Za-z\s]+$/.test(val.trim()); }
    function isValidPhone(val) { return /^\d{10}$/.test(val.trim()); }
    function isValidPositiveNum(val) { const n = Number(val); return Number.isFinite(n) && n > 0; }
    function isValidPositiveInt(val) { const n = Number(val); return Number.isInteger(n) && n > 0; }
    function isValidEmail(val) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val.trim()); }
    function isValidDate(val) {
        if (!val) return false;
        const sel = new Date(`${val}T00:00:00`);
        const today = new Date();
        today.setHours(0,0,0,0);
        return !Number.isNaN(sel.getTime()) && sel <= today;
    }

    function getFormData(form) {
        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            const el = form.elements[key];
            if (value && el && el.type === 'number' && !isNaN(value)) {
                data[key] = Number(value);
            } else {
                data[key] = value;
            }
        }
        return data;
    }

    async function handleFormSubmit(event, url, validator, reloadFn, modalId) {
        event.preventDefault();
        const form = event.currentTarget;
        
        // Basic pre-validation matching existing rules
        if (validator && !validator(form)) return;

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...';

        try {
            const data = getFormData(form);
            const response = await fetch(`http://localhost:8000${url}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errData = await response.json().catch(()=>({}));
                let msg = errData.message || errData.error || `Error ${response.status}`;
                throw new Error(msg);
            }

            showToast('Record saved successfully!');
            form.reset();
            
            // Close modal
            const modalEl = document.getElementById(modalId);
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) modalInstance.hide();

            // Refresh table
            if (reloadFn) reloadFn();

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }

    // -----------------------------------------
    // Specific Form Validators
    // -----------------------------------------
    const validateFarmer = (f) => {
        if (!isValidName(f.elements['full_name'].value)) { showToast("Name can only contain letters and spaces.", "error"); return false; }
        if (!isValidPhone(f.elements['phone'].value)) { showToast("Phone must be exactly 10 digits.", "error"); return false; }
        const em = f.elements['email'].value;
        if (em && !isValidEmail(em)) { showToast("Invalid email address.", "error"); return false; }
        return true;
    };
    
    const validateCattle = (f) => {
        if (!isValidPositiveInt(f.elements['farmer_id'].value)) { showToast("Invalid Farmer ID.", "error"); return false; }
        const dob = f.elements['date_of_birth'].value;
        if (dob && !isValidDate(dob)) { showToast("Date of Birth cannot be in the future.", "error"); return false; }
        return true;
    };
    
    const validateMilk = (f) => {
        if (!isValidDate(f.elements['record_date'].value)) { showToast("Date cannot be in the future.", "error"); return false; }
        if (!isValidPositiveNum(f.elements['quantity_litres'].value)) { showToast("Quantity must be greater than 0.", "error"); return false; }
        return true;
    };

    const validateFeed = (f) => {
        if (!isValidDate(f.elements['record_date'].value)) { showToast("Date cannot be in the future.", "error"); return false; }
        if (!isValidPositiveNum(f.elements['quantity_kg'].value)) { showToast("Quantity must be greater than 0.", "error"); return false; }
        if (!isValidPositiveNum(f.elements['cost'].value)) { showToast("Cost must be greater than 0.", "error"); return false; }
        return true;
    };

    const validateExpense = (f) => {
        if (!isValidDate(f.elements['expense_date'].value)) { showToast("Date cannot be in the future.", "error"); return false; }
        if (!isValidPositiveNum(f.elements['amount'].value)) { showToast("Amount must be greater than 0.", "error"); return false; }
        return true;
    };

    const validateRevenue = (f) => {
        if (!isValidDate(f.elements['sale_date'].value)) { showToast("Date cannot be in the future.", "error"); return false; }
        if (!isValidPositiveNum(f.elements['quantity_litres'].value)) { showToast("Quantity must be greater than 0.", "error"); return false; }
        if (!isValidPositiveNum(f.elements['price_per_litre'].value)) { showToast("Price must be greater than 0.", "error"); return false; }
        return true;
    };

    // -----------------------------------------
    // Attach Submit Listeners
    // -----------------------------------------
    document.getElementById('farmer-form')?.addEventListener('submit', e => handleFormSubmit(e, '/api/farmers', validateFarmer, loadFarmers, 'farmerModal'));
    document.getElementById('cattle-form')?.addEventListener('submit', e => handleFormSubmit(e, '/api/cattle', validateCattle, loadCattle, 'cattleModal'));
    document.getElementById('milk-form')?.addEventListener('submit', e => handleFormSubmit(e, '/api/milk-records', validateMilk, loadMilkRecords, 'milkModal'));
    document.getElementById('feed-form')?.addEventListener('submit', e => handleFormSubmit(e, '/api/feed-records', validateFeed, loadFeedRecords, 'feedModal'));
    document.getElementById('expense-form')?.addEventListener('submit', e => handleFormSubmit(e, '/api/expenses', validateExpense, loadExpenses, 'expenseModal'));
    document.getElementById('revenue-form')?.addEventListener('submit', e => handleFormSubmit(e, '/api/revenue', validateRevenue, loadRevenue, 'revenueModal'));
});
