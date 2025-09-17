js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector("#budgetForm");
    const resultDiv = document.querySelector("#result");

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Отменяем стандартную отправку формы

        const income = document.querySelector("#income").value;
        const expenses = document.querySelector("#expenses").value;

        const res = await fetch("/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                income,
                expenses
            })
        });

        const data = await res.json();
        resultDiv.textContent = `Ваш бюджет: ₽${data.balance}`;
    });
});