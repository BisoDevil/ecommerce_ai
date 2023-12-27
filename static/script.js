
function submitForm() {

    var input = document.getElementById("input").value;
    var desc = document.getElementById("desc").value;
    var bullets = document.getElementById("bullets").value;


    var url = "/generate";
    var url_predict = "/predict"; // Replace with the Flask endpoint URL

    var xhr = new XMLHttpRequest();
    var loadingIcon = document.createElement("i");
    loadingIcon.classList.add("fa", "fa-spinner", "fa-spin");
    loadingIcon.setAttribute("aria-hidden", "true");


    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<br><p style='font-size: 12px' >Generating product content, This process may take some long time be patient...</p>";
    resultDiv.appendChild(loadingIcon);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the API response here
            var response = JSON.parse(xhr.responseText);
            var resultDiv = document.getElementById("result");
            const markdownText = response['message'];
            const converter = new showdown.Converter();
            const html = converter.makeHtml(markdownText);

            resultDiv.innerHTML = html;
            // resultDiv.innerHTML = "<h3>Product information:</h3><br>" + response['message'];
        }
    };
    xhr.send(JSON.stringify({ text: input + " " + desc, bullet: bullets }));

    var xhr2 = new XMLHttpRequest();
    xhr2.open("POST", url_predict, true);
    xhr2.setRequestHeader("Content-Type", "application/json");

    xhr2.onreadystatechange = function () {
        if (xhr2.readyState === 4 && xhr2.status === 200) {
            // Handle the API response here
            var response = JSON.parse(xhr2.responseText);
            var categoryDiv = document.getElementById("category");
            categoryDiv.innerHTML = "<strong>Category:</strong>" + response['category'];


        }
    };
    xhr2.send(JSON.stringify({ texts: [input] }));


    return false;
}
