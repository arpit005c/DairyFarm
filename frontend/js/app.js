"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const modulesHeading = document.getElementById("modules-heading");
    const forms = document.querySelectorAll("form");

    function initializeModulesHeading() {
        if (!modulesHeading) {
            return;
        }

        modulesHeading.textContent = "System Modules";
    }

    function isValidName(value) {
        return /^[A-Za-z\s]+$/.test(value.trim());
    }

    function isValidPhone(value) {
        return /^\d{10}$/.test(value.trim());
    }

    function isValidPositiveNumber(value) {
        const number = Number(value);

        return Number.isFinite(number) && number > 0;
    }

    function isValidPositiveInteger(value) {
        const number = Number(value);

        return Number.isInteger(number) && number > 0;
    }

    function isValidEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
    }

    function isValidDateNotInFuture(value) {
        if (!value) {
            return false;
        }

        const selectedDate = new Date(`${value}T00:00:00`);
        const today = new Date();

        today.setHours(0, 0, 0, 0);

        return (
            !Number.isNaN(selectedDate.getTime()) &&
            selectedDate <= today
        );
    }

    function handleFarmerValidation(form) {
        const fullName = form.elements["full_name"].value.trim();
        const phone = form.elements["phone"].value.trim();
        const email = form.elements["email"].value.trim();
        const address = form.elements["address"].value.trim();

        if (fullName.length === 0) {
            alert(
                "Full Name is required. Please enter the farmer's full name."
            );
            return false;
        }

        if (!isValidName(fullName)) {
            alert("Full Name can contain letters and spaces only.");
            return false;
        }

        if (phone.length === 0) {
            alert(
                "Phone Number is required. Please enter a 10-digit phone number."
            );
            return false;
        }

        if (!/^\d+$/.test(phone)) {
            alert("Phone Number must contain digits only.");
            return false;
        }

        if (!isValidPhone(phone)) {
            alert("Phone Number must be exactly 10 digits.");
            return false;
        }

        if (email.length === 0) {
            alert(
                "Email Address is required. Please enter the farmer's email address."
            );
            return false;
        }

        if (!isValidEmail(email)) {
            alert(
                "Please enter a valid Email Address (example: name@example.com)."
            );
            return false;
        }

        if (address.length === 0) {
            alert(
                "Address is required. Please enter the farmer's address."
            );
            return false;
        }

        return true;
    }

    function handleCattleValidation(form) {
        const farmerId = form.elements["farmer_id"].value.trim();
        const tagNumber = form.elements["tag_number"].value.trim();
        const gender = form.elements["gender"].value;
        const cattleName = form.elements["name"].value.trim();
        const breed = form.elements["breed"].value.trim();
        const dateOfBirth = form.elements["date_of_birth"].value;
        const status = form.elements["status"].value;

        if (farmerId.length === 0) {
            alert(
                "Farmer ID is required. Please enter the farmer ID."
            );
            return false;
        }

        if (!isValidPositiveInteger(farmerId)) {
            alert(
                "Farmer ID must be a positive whole number."
            );
            return false;
        }

        if (tagNumber.length === 0) {
            alert(
                "Tag Number is required. Please enter the cattle tag number."
            );
            return false;
        }

        if (gender.length === 0) {
            alert(
                "Gender is required. Please select the cattle gender."
            );
            return false;
        }

        if (gender !== "male" && gender !== "female") {
            alert(
                "Please select a valid cattle gender."
            );
            return false;
        }

        if (cattleName.length > 0 && !isValidName(cattleName)) {
            alert(
                "Cattle Name can contain letters and spaces only."
            );
            return false;
        }

        if (breed.length > 0 && !isValidName(breed)) {
            alert(
                "Breed can contain letters and spaces only."
            );
            return false;
        }

        if (
            dateOfBirth.length > 0 &&
            !isValidDateNotInFuture(dateOfBirth)
        ) {
            alert(
                "Date of Birth cannot be a future date."
            );
            return false;
        }

        if (status !== "active" && status !== "inactive") {
            alert(
                "Please select a valid cattle status."
            );
            return false;
        }

        return true;
    }

    function handleMilkRecordValidation(form) {
        const cattleId = form.elements["cattle_id"].value.trim();
        const recordDate = form.elements["record_date"].value;
        const session = form.elements["session"].value;
        const quantity = form.elements["quantity_litres"].value.trim();

        if (cattleId.length === 0) {
            alert(
                "Cattle ID is required. Please enter the cattle ID."
            );
            return false;
        }

        if (!isValidPositiveInteger(cattleId)) {
            alert(
                "Cattle ID must be a positive whole number."
            );
            return false;
        }

        if (recordDate.length === 0) {
            alert(
                "Record Date is required. Please select the milk record date."
            );
            return false;
        }

        if (!isValidDateNotInFuture(recordDate)) {
            alert(
                "Record Date cannot be a future date."
            );
            return false;
        }

        if (session.length === 0) {
            alert(
                "Session is required. Please select Morning or Evening."
            );
            return false;
        }

        if (session !== "morning" && session !== "evening") {
            alert(
                "Please select a valid milk recording session."
            );
            return false;
        }

        if (quantity.length === 0) {
            alert(
                "Milk Quantity is required. Please enter the quantity in litres."
            );
            return false;
        }

        if (!isValidPositiveNumber(quantity)) {
            alert(
                "Milk Quantity must be a positive number greater than 0."
            );
            return false;
        }

        return true;
    }
    function handleFeedRecordValidation(form) {
    const farmerId = form.elements["farmer_id"].value.trim();
    const cattleId = form.elements["cattle_id"].value.trim();
    const recordDate = form.elements["record_date"].value;
    const feedType = form.elements["feed_type"].value.trim();
    const quantity = form.elements["quantity_kg"].value.trim();
    const cost = form.elements["cost"].value.trim();

    if (farmerId.length === 0) {
        alert(
            "Farmer ID is required. Please enter the farmer ID."
        );
        return false;
    }

    if (!isValidPositiveInteger(farmerId)) {
        alert(
            "Farmer ID must be a positive whole number."
        );
        return false;
    }

    if (cattleId.length === 0) {
        alert(
        "Cattle ID is required. Please enter the cattle ID."
        );
        return false;
    }

    if (!isValidPositiveInteger(cattleId)) {
        alert(
        "Cattle ID must be a positive whole number."
        );
        return false;
    }

    if (recordDate.length === 0) {
        alert(
            "Record Date is required. Please select the feed record date."
        );
        return false;
    }

    if (!isValidDateNotInFuture(recordDate)) {
        alert(
            "Record Date cannot be a future date."
        );
        return false;
    }

    if (feedType.length === 0) {
        alert(
            "Feed Type is required. Please enter the type of feed."
        );
        return false;
    }

    if (!isValidName(feedType)) {
        alert(
            "Feed Type can contain letters and spaces only."
        );
        return false;
    }

    if (quantity.length === 0) {
        alert(
            "Quantity is required. Please enter the feed quantity in kilograms."
        );
        return false;
    }

    if (!isValidPositiveNumber(quantity)) {
        alert(
            "Quantity must be a positive number greater than 0."
        );
        return false;
    }

    if (cost.length === 0) {
        alert(
            "Cost is required. Please enter the feed cost."
        );
        return false;
    }

    if (!isValidPositiveNumber(cost)) {
        alert(
            "Cost must be a positive number greater than 0."
        );
        return false;
    }

    return true;
    }
    function handleExpenseValidation(form) {
    const farmerId = form.elements["farmer_id"].value.trim();
    const expenseDate = form.elements["expense_date"].value;
    const category = form.elements["category"].value.trim();
    const amount = form.elements["amount"].value.trim();
    const description = form.elements["description"].value.trim();

    if (farmerId.length === 0) {
        alert(
            "Farmer ID is required. Please enter the farmer ID."
        );
        return false;
    }

    if (!isValidPositiveInteger(farmerId)) {
        alert(
            "Farmer ID must be a positive whole number."
        );
        return false;
    }

    if (expenseDate.length === 0) {
        alert(
            "Expense Date is required. Please select the expense date."
        );
        return false;
    }

    if (!isValidDateNotInFuture(expenseDate)) {
        alert(
            "Expense Date cannot be a future date."
        );
        return false;
    }

    if (category.length === 0) {
        alert(
            "Category is required. Please enter the expense category."
        );
        return false;
    }

    if (!isValidName(category)) {
        alert(
            "Category can contain letters and spaces only."
        );
        return false;
    }

    if (amount.length === 0) {
        alert(
            "Amount is required. Please enter the expense amount."
        );
        return false;
    }

    if (!isValidPositiveNumber(amount)) {
        alert(
            "Amount must be a positive number greater than 0."
        );
        return false;
    }

    if (description.length === 0) {
        alert(
            "Description is required. Please enter a description of the expense."
        );
        return false;
    }

    return true;
}
    function handleRevenueValidation(form) {
    const farmerId = form.elements["farmer_id"].value.trim();
    const saleDate = form.elements["sale_date"].value;
    const quantity = form.elements["quantity_litres"].value.trim();
    const pricePerLitre = form.elements["price_per_litre"].value.trim();
    const buyerName = form.elements["buyer_name"].value.trim();

    if (farmerId.length === 0) {
        alert(
            "Farmer ID is required. Please enter the farmer ID."
        );
        return false;
    }

    if (!isValidPositiveInteger(farmerId)) {
        alert(
            "Farmer ID must be a positive whole number."
        );
        return false;
    }

    if (saleDate.length === 0) {
        alert(
            "Sale Date is required. Please select the sale date."
        );
        return false;
    }

    if (!isValidDateNotInFuture(saleDate)) {
        alert(
            "Sale Date cannot be a future date."
        );
        return false;
    }

    if (quantity.length === 0) {
        alert(
            "Quantity is required. Please enter the quantity in litres."
        );
        return false;
    }

    if (!isValidPositiveNumber(quantity)) {
        alert(
            "Quantity must be a positive number greater than 0."
        );
        return false;
    }

    if (pricePerLitre.length === 0) {
        alert(
            "Price per Litre is required. Please enter the price per litre."
        );
        return false;
    }

    if (!isValidPositiveNumber(pricePerLitre)) {
        alert(
            "Price per Litre must be a positive number greater than 0."
        );
        return false;
    }

    if (buyerName.length === 0) {
    alert(
        "Buyer Name is required. Please enter the buyer's name."
    );
    return false;
    }

    if (!isValidName(buyerName)) {
    alert(
        "Buyer Name can contain letters and spaces only."
    );
    return false;
    }

    return true;
}

    function handleFormSubmit(event) {
        event.preventDefault();

        const form = event.currentTarget;
        const module = form.closest("article");

        if (!module) {
            return;
        }

        if (module.id === "farmers") {
            const isValid = handleFarmerValidation(form);

            if (!isValid) {
                return;
            }

            console.log("Farmer form validation successful.");
            return;
        }

        if (module.id === "cattle") {
            const isValid = handleCattleValidation(form);

            if (!isValid) {
                return;
            }

            console.log("Cattle form validation successful.");
            return;
        }

        if (module.id === "milk-records") {
            const isValid = handleMilkRecordValidation(form);

            if (!isValid) {
                return;
            }

            console.log("Milk Record form validation successful.");
            return;
        }
        if (module.id === "feed-records") {
            const isValid = handleFeedRecordValidation(form);

            if (!isValid) {
                return;
            }

        console.log("Feed Record form validation successful.");
        return;
        }
        if (module.id === "expenses") {
            const isValid = handleExpenseValidation(form);

            if (!isValid) {
            return;
            }

            console.log("Expense form validation successful.");
        return;
        }

        if (module.id === "revenue") {
            const isValid = handleRevenueValidation(form);

            if (!isValid) {
            return;
        }

        console.log("Revenue form validation successful.");
        return;
        }

        console.log(`Form submitted: ${module.id}`);
    }

    function initializeFormHandlers() {
        forms.forEach((form) => {
            form.addEventListener("submit", handleFormSubmit);
        });
    }

    initializeModulesHeading();
    initializeFormHandlers();

    console.log("DairyFarm JavaScript loaded successfully.");
});
