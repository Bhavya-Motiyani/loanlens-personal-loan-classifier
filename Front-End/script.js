setTimeout(() => {

    const splash = document.getElementById("splash");

    splash.style.opacity = "0";

    setTimeout(() => {

        splash.style.display = "none";

        document.getElementById("mainScreen").style.display = "flex";

        // document.body.style.overflowX = "hidden";
        // document.body.style.overflowY = "hidden";

    }, 1000);

}, 3000);

function showPage(page) {

    const predict = document.getElementById("predictionpage");
    const analysis = document.getElementById("analysispage");
    const navButtons = document.querySelectorAll('.buttons button');
    const activeClasses = ["bg-fuchsia-300/10", "px-2", "py-1", "rounded-lg"];

    predict.classList.add("hidden");
    analysis.classList.add("hidden");

    navButtons.forEach(btn => {
        btn.classList.remove(...activeClasses);
    });

    if (page === "predict") {
        predict.classList.remove("hidden");
        navButtons[0].classList.add(...activeClasses);
    }

    if (page === "analysis") {
        analysis.classList.remove("hidden");
        navButtons[1].classList.add(...activeClasses);
    }
}

function setGauge(value) {

    const gauge = document.getElementById("gauge");
    const text = document.getElementById("percentageText");

    const degree = (value / 100) * 360;

    let startColor = "";
    let middleColor = "";
    let endColor = "";
    let textGlow = "";

    if (value < 40) {

        startColor = "#ff0055";
        middleColor = "#ff4d4d";
        endColor = "#ff7b00";

        textGlow = "0 0 20px rgba(255,0,85,0.8)";
    }

    else if (value < 70) {

        startColor = "#ffb800";
        middleColor = "#ff7b00";
        endColor = "#ff3d77";

        textGlow = "0 0 20px rgba(255,184,0,0.8)";
    }

    else {

        startColor = "#00e5ff";
        middleColor = "#00ffae";
        endColor = "#7dff3c";

        textGlow = "0 0 25px rgba(0,255,174,0.9)";
    }

    gauge.style.background = `
    conic-gradient(
        from 180deg,

        ${startColor} 0deg,
        ${middleColor} ${degree * 0.6}deg,
        ${endColor} ${degree}deg,

        #1e293b ${degree}deg,
        #1e293b 360deg
    )
`;

    text.innerText = value + "%";

    text.style.background = `
      linear-gradient(
        to right,
        #ffffff,
        #7df9ff
      )
    `;

    text.style.webkitBackgroundClip = "text";
    text.style.webkitTextFillColor = "transparent";

    text.style.textShadow = textGlow;
}

const predictionPercentage = 100;

setGauge(predictionPercentage);

function renderAnalysis(data) {

  const container = document.getElementById("analysisContainer");

  container.innerHTML = "";

  data.forEach(item => {

    // Convert impact into width
    const width = Math.max(item.impact * 900, 10);

    // Positive / Negative colors
    const isPositive = item.impact >= 0;

    const gradient = isPositive
      ? "linear-gradient(to right, #ff2d95, #ff1f5a)"
      : "linear-gradient(to right, #00d2ff, #3a86ff)";

    const valueColor = isPositive
      ? "text-pink-300"
      : "text-cyan-300";

    container.innerHTML += `

      <div class="flex items-center gap-1">

        <!-- LEFT TEXT -->
        <div class="w-45 text-right text-slate-300 text-[10px]">

          <span class="text-slate-500 text-[10px]">
            ${item.value}
          </span>

          =
          
          <span class="font-bold text-white text-[10px]">
            ${item.feature}
          </span>

        </div>

        <!-- BAR -->
        <div class="flex-1 h-3 bg-[#121c38] rounded-full overflow-hidden">

          <div
            class="h-3 rounded-full transition-all duration-1000"
            style="
              width:${width}px;
              background:${gradient};
              box-shadow:0 0 20px rgba(255,255,255,0.15);
            "
          ></div>

        </div>

        <!-- IMPACT VALUE -->
        <div class="${valueColor} font-bold w-15 text-[10px] text-right">

          ${item.impact > 0 ? "+" : ""}
          ${item.impact.toFixed(2)}

        </div>

      </div>
    `;
  });
}

const predictBtn = document.getElementById("predictBtn");

predictBtn.addEventListener("click", async () => {

    const age = document.getElementById("age").value;
    const income = document.getElementById("income").value;
    const ccavg = document.getElementById("ccavg").value;
    const cd_account = document.getElementById("cdaccount").value;
    const mortgage = document.getElementById("mortgage").value;
    const education = document.getElementById("education").value;

    try {

        const response = await fetch("http://127.0.0.1:5000/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                age,
                income,
                ccavg,
                cd_account,
                mortgage,
                education
            })

        });

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        console.log(data);
        renderAnalysis(data.analysis);

        const probability = Math.round(data.probability * 100);

        const finalScore = document.getElementById("finalScore");

        finalScore.innerText = data.probability.toFixed(3);
        if (data.probability > 0.7) {

            finalScore.classList.remove("text-red-400", "text-yellow-400");
            finalScore.classList.add("text-green-400");

        }

        else if (data.probability > 0.4) {

            finalScore.classList.remove("text-red-400", "text-green-400");
            finalScore.classList.add("text-yellow-400");

        }

        else {

            finalScore.classList.remove("text-green-400", "text-yellow-400");
            finalScore.classList.add("text-red-400");

        }

        setGauge(probability);

        const resultText = document.getElementById("resultText");

        const resultDescription =
            document.getElementById("resultDescription");

        if (data.prediction === 1) {

            resultText.innerText = "Accept";

            resultText.classList.remove("text-red-400");

            resultText.classList.add("text-green-400");

            resultDescription.innerText =
                "Customer is highly likely to accept the personal loan offer.";

        }

        else {

            resultText.innerText = "Reject";

            resultText.classList.remove("text-green-400");

            resultText.classList.add("text-red-400");

            resultDescription.innerText =
                "Customer is unlikely to accept the personal loan offer.";

        }

    }

    catch(error) {

        console.log(error);

        alert("Prediction failed");

    }

});
