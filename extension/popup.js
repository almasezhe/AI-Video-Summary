document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const url = document.getElementById('youtubeUrl').value;
    const loader = document.getElementById('loader');
    const resultDiv = document.getElementById('result');

    if (!url) {
        alert("Вставь ссылку!");
        return;
    }

    loader.style.display = 'block';
    resultDiv.style.display = 'none';
    resultDiv.innerText = '';

    try {
        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ youtube_url: url })
        });

        const data = await response.json();

        loader.style.display = 'none';
        resultDiv.style.display = 'block';
        resultDiv.innerText = data.result;

    } catch (error) {
        loader.style.display = 'none';
        alert("Ошибка при анализе видео!");
        console.error(error);
    }
});
