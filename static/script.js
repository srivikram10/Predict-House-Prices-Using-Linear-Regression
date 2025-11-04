document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent full page reload

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Client-side validation
    if (data.area <= 0 || data.bedrooms < 1 || data.bathrooms < 1 || data.sqft <= 0) {
        alert('⚠️ Please enter valid positive numbers!');
        return;
    }

    const resultDiv = document.getElementById('result');
    const loading = document.getElementById('loading');
    resultDiv.textContent = '';
    loading.style.display = 'block';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const json = await response.json();

        if (json.prediction) {
            resultDiv.textContent = json.prediction;
            resultDiv.style.opacity = 0;
            setTimeout(() => { resultDiv.style.transition = 'opacity 1s'; resultDiv.style.opacity = 1; }, 100);
        } else {
            resultDiv.textContent = json.error || '⚠️ Prediction failed.';
            resultDiv.style.color = 'red';
        }
    } catch (err) {
        resultDiv.textContent = '⚠️ Network error: ' + err.message;
        resultDiv.style.color = 'red';
    } finally {
        loading.style.display = 'none';
    }
});