function installBenefitCalculator() {
    const base_bonus = 300000;
    const multiple_child_coefficient = 1.5;
    const valorization_rate = 0.04; // estimate
    const base_year = 2020;
    const revenue_period_absolute_min = 7;
    const revenue_period_default_min = 30;
    const revenue_period_absolute_max = 48;

    var compute_total_button = document.querySelector(
        'button[id="compute_total"]'
    );
    var compute_monthly_button = document.querySelector(
        'button[id="compute_monthly"]'
    );

    var claim_date_input = document.querySelector('input[id="claim_date"]'); // min: 2020-01-01
    var multiple_children_input = document.querySelector(
        'input[id="multiple_children"]'
    );
    var period_of_revenue_input = document.querySelector(
        'input[id="period_of_revenue"]'
    );
    var gross_monthly_income_input = document.querySelector(
        'input[id="gross_monthly_income"]'
    );

    var total_bonus_output = document.querySelector('input[id="total_bonus"]');
    var monthly_bonus_output = document.querySelector(
        'input[id="monthly_bonus"]'
    );
    var period_of_revenue_min_output = document.querySelector(
        'input[id="period_of_revenue_min"]'
    );
    var period_of_revenue_max_output = document.querySelector(
        'input[id="period_of_revenue_max"]'
    );

    var results = document.querySelector('div[id="compute_results"]')
    var resultsMonthly = document.querySelector('div[id="compute_final_results"]')

    var parents_bonus_div = document.querySelector('div[id="parents_bonus"]');

    function updateMonthly() {
        monthly_bonus_output.value = Math.ceil(
            total_bonus_output.value / period_of_revenue_input.value
        );
    }

    compute_total_button.onclick = function() {
        var claim_date = new Date(claim_date_input.value);
        var multiple_children = multiple_children_input.checked;
        var gross_monthly_income = gross_monthly_income_input.value; // higher of the parents

        var valorization_years = claim_date.getFullYear() - base_year;
        var valorization_months = claim_date.getMonth() + 1;
        var number_of_children_coefficient;
        if (multiple_children) {
            number_of_children_coefficient = multiple_child_coefficient;
        } else {
            number_of_children_coefficient = 1;
        }

        var valorized_bonus;
        if (valorization_years > 0) {
            var valorized_base =
                base_bonus *
                number_of_children_coefficient *
                Math.pow(1 + valorization_rate, valorization_years - 1);
            valorized_bonus =
                valorized_base *
                (1 + (valorization_rate * valorization_months) / 12);
        } else {
            valorized_bonus = base_bonus * number_of_children_coefficient;
        }

        total_bonus_output.value = Math.ceil(valorized_bonus);

        var monthly_max_bonus = gross_monthly_income * 0.7;
        var period_of_revenue_min = Math.min(
            Math.max(
                revenue_period_absolute_min,
                Math.ceil(valorized_bonus / monthly_max_bonus)
            ),
            revenue_period_default_min
        );
        var period_of_revenue_max = revenue_period_absolute_max;

        period_of_revenue_input.min = period_of_revenue_min_output.value = period_of_revenue_min;
        period_of_revenue_input.max = period_of_revenue_max_output.value = period_of_revenue_max;
        period_of_revenue_input.value = period_of_revenue_min;

        period_of_revenue_input.onchange = updateMonthly;
        results.style.display = "block";

        updateMonthly();
    };

    parents_bonus_div.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            compute_total_button.click();
        }
    });
}


module.exports = installBenefitCalculator;
