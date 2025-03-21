document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const sortBy = document.getElementById("sortBy");
    const sortOrder = document.getElementById("sortOrder");
    const transactionTableBody = document.getElementById("transactionTableBody");

    if (!searchInput || !sortBy || !sortOrder || !transactionTableBody) {
        console.error("Required elements are missing from the page.");
        return;
    }

    function loadTransactions() {
        const search = encodeURIComponent(searchInput.value.trim());
        const sort = encodeURIComponent(sortBy.value);
        const order = encodeURIComponent(sortOrder.value);

        fetch(`/ott_subscription/api/transactions/?search=${search}&sort_by=${sort}&sort_order=${order}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                transactionTableBody.innerHTML = "";

                if (!data.transactions || data.transactions.length === 0) {
                    transactionTableBody.innerHTML = `<tr><td colspan="8" class="text-center">No transactions found</td></tr>`;
                    return;
                }

                transactionTableBody.innerHTML = data.transactions.map(t => `
                    <tr>
                        <td>${t.client_id}</td>
                        <td>${t.platform}</td>
                        <td>${t.plan_id}</td>
                        <td>${t.activation_date}</td>
                        <td>${t.status}</td>
                        <td>${t.subscription_tiers}</td>
                        <td>${t.payment_amount}</td>
                        <td>${t.expiration_date}</td>
                    </tr>
                `).join("");
            })
            .catch(error => {
                console.error("Error loading transactions:", error);
                transactionTableBody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Failed to load transactions</td></tr>`;
            });
    }

    searchInput.addEventListener("input", loadTransactions);
    sortBy.addEventListener("change", loadTransactions);
    sortOrder.addEventListener("change", loadTransactions);

    loadTransactions();  // Initial load
});
