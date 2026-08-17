// =========================================
// TRACKX FRONTEND SCRIPT
// =========================================

const API_URL = "http://127.0.0.1:8000";


// =========================================
// CURRENT DATE & TIME
// =========================================

function updateDateTime() {

    const now = new Date();

    const time = now.toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit"
    });

    const date = now.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });

    const timeElement =
        document.getElementById("currentTime");

    const dateElement =
        document.getElementById("currentDate");

    if (timeElement) {
        timeElement.textContent = time;
    }

    if (dateElement) {
        dateElement.textContent = date;
    }
}

updateDateTime();

setInterval(updateDateTime, 1000);


// =========================================
// DEFAULT DATE & TIME
// =========================================

function setDefaultDateTime() {

    const dateInput =
        document.getElementById("journeyDate");

    const timeInput =
        document.getElementById("journeyTime");

    if (!dateInput || !timeInput) {
        return;
    }

    const now = new Date();

    const year =
        now.getFullYear();

    const month =
        String(now.getMonth() + 1)
            .padStart(2, "0");

    const day =
        String(now.getDate())
            .padStart(2, "0");

    const hours =
        String(now.getHours())
            .padStart(2, "0");

    const minutes =
        String(now.getMinutes())
            .padStart(2, "0");


    dateInput.value =
        `${year}-${month}-${day}`;

    timeInput.value =
        `${hours}:${minutes}`;
}

setDefaultDateTime();


// =========================================
// LOAD STATIONS
// =========================================

async function loadStations() {

    try {

        const response =
            await fetch(`${API_URL}/stations`);

        if (!response.ok) {

            throw new Error(
                "Unable to load stations"
            );
        }


        const data =
            await response.json();


        const fromStation =
            document.getElementById("fromStation");

        const toStation =
            document.getElementById("toStation");


        if (!fromStation || !toStation) {
            return;
        }


        fromStation.innerHTML =
            `<option value="">Select Station</option>`;

        toStation.innerHTML =
            `<option value="">Select Station</option>`;


        data.stations.forEach(station => {

            const option1 =
                document.createElement("option");

            option1.value =
                station.id;

            option1.textContent =
                station.name;

            fromStation.appendChild(option1);


            const option2 =
                document.createElement("option");

            option2.value =
                station.id;

            option2.textContent =
                station.name;

            toStation.appendChild(option2);

        });


        console.log(
            "Stations loaded successfully"
        );


    } catch (error) {

        console.error(
            "Station loading error:",
            error
        );
    }
}

loadStations();


// =========================================
// SWAP STATIONS
// =========================================

const swapButton =
    document.getElementById("swapButton");


if (swapButton) {

    swapButton.addEventListener(
        "click",
        () => {

            const fromStation =
                document.getElementById("fromStation");

            const toStation =
                document.getElementById("toStation");


            if (!fromStation || !toStation) {
                return;
            }


            const temporaryValue =
                fromStation.value;


            fromStation.value =
                toStation.value;

            toStation.value =
                temporaryValue;
        }
    );
}


// =========================================
// FIND TRAINS
// =========================================

const findTrainsButton =
    document.getElementById("findTrainsButton");


if (findTrainsButton) {

    findTrainsButton.addEventListener(
        "click",
        async () => {

            const fromStation =
                document.getElementById("fromStation");

            const toStation =
                document.getElementById("toStation");

            const date =
                document.getElementById("journeyDate");

            const time =
                document.getElementById("journeyTime");

            const trainList =
                document.getElementById("trainList");


            if (
                !fromStation ||
                !toStation ||
                !trainList
            ) {
                return;
            }


            // -----------------------------
            // VALIDATION
            // -----------------------------

            if (
                !fromStation.value ||
                !toStation.value
            ) {

                alert(
                    "Please select both stations."
                );

                return;
            }


            if (
                fromStation.value ===
                toStation.value
            ) {

                alert(
                    "From and To stations cannot be the same."
                );

                return;
            }


            if (
                date &&
                time &&
                (!date.value || !time.value)
            ) {

                alert(
                    "Please select date and time."
                );

                return;
            }


            // -----------------------------
            // LOADING
            // -----------------------------

            trainList.innerHTML = `
                <p class="no-trains">
                    Finding trains...
                </p>
            `;


            try {

                const response =
                    await fetch(
                        `${API_URL}/find-trains?from_station=${fromStation.value}&to_station=${toStation.value}`
                    );


                if (!response.ok) {

                    throw new Error(
                        "Unable to find trains"
                    );
                }


                const data =
                    await response.json();


                // -----------------------------
                // NO TRAINS
                // -----------------------------

                if (
                    !data.trains ||
                    data.trains.length === 0
                ) {

                    trainList.innerHTML = `
                        <p class="no-trains">
                            No available trains found
                            for this journey.
                        </p>
                    `;

                    return;
                }


                // -----------------------------
                // DISPLAY TRAINS
                // -----------------------------

                trainList.innerHTML = "";


                const fromName =
                    fromStation.options[
                        fromStation.selectedIndex
                    ].text;


                const toName =
                    toStation.options[
                        toStation.selectedIndex
                    ].text;


                data.trains.forEach(train => {

                    const trainRow =
                        document.createElement("div");


                    trainRow.className =
                        "train-row";


                    trainRow.innerHTML = `

                        <div class="train-icon">
                            🚇
                        </div>

                        <div class="train-info">

                            <strong>
                                ${train.name}
                            </strong>

                            <span>
                                ${fromName} ↔ ${toName}
                            </span>

                        </div>

                        <div class="running-status">

                            <span></span>

                            Running

                        </div>

                    `;


                    trainList.appendChild(
                        trainRow
                    );

                });


                // -----------------------------
                // SCROLL TO RESULTS
                // -----------------------------

                const trainsSection =
                    document.getElementById("trains");


                if (trainsSection) {

                    trainsSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }


            } catch (error) {

                console.error(
                    "Train search error:",
                    error
                );


                trainList.innerHTML = `
                    <p class="no-trains">
                        Unable to connect to TrackX backend.
                    </p>
                `;
            }

        }
    );
}


// =========================================
// LOAD TRAINS
// =========================================

async function loadTrains() {

    try {

        const response =
            await fetch(`${API_URL}/trains`);


        if (!response.ok) {

            throw new Error(
                "Unable to load trains"
            );
        }


        const data =
            await response.json();


        console.log(
            "Trains loaded:",
            data
        );


    } catch (error) {

        console.error(
            "Train loading error:",
            error
        );
    }
}

loadTrains();


// =========================================
// EMPLOYEE LOGIN
// =========================================

const employeeLoginButton =
    document.getElementById(
        "employeeLoginButton"
    );


if (employeeLoginButton) {

    employeeLoginButton.addEventListener(
        "click",
        async () => {

            const usernameInput =
                document.getElementById(
                    "employeeUsername"
                );

            const passwordInput =
                document.getElementById(
                    "employeePassword"
                );

            const message =
                document.getElementById(
                    "loginMessage"
                );


            if (
                !usernameInput ||
                !passwordInput ||
                !message
            ) {
                return;
            }


            const username =
                usernameInput.value.trim();

            const password =
                passwordInput.value;


            // -----------------------------
            // VALIDATION
            // -----------------------------

            if (!username || !password) {

                message.textContent =
                    "Please enter username and password.";

                return;
            }


            try {

                console.log(
                    "Attempting employee login..."
                );


                const response =
                    await fetch(
                        `${API_URL}/employee/login`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                username:
                                    username,

                                password:
                                    password
                            })
                        }
                    );


                const data =
                    await response.json();


                console.log(
                    "Login response:",
                    data
                );


                if (!response.ok) {

                    message.textContent =
                        data.detail ||
                        "Login failed.";

                    return;
                }


                // -----------------------------
                // SAVE TOKEN
                // -----------------------------

                localStorage.setItem(
                    "trackx_employee_token",
                    data.access_token
                );


                console.log(
                    "Employee login successful."
                );


                // -----------------------------
                // HIDE LOGIN
                // -----------------------------

                const loginBox =
                    document.getElementById(
                        "employeeLogin"
                    );


                if (loginBox) {

                    loginBox.style.display =
                        "none";
                }


                // -----------------------------
                // SHOW DASHBOARD
                // -----------------------------

                const dashboard =
                    document.getElementById(
                        "employeeDashboard"
                    );


                if (dashboard) {

                    dashboard.style.display =
                        "block";
                }


                message.textContent = "";


                // -----------------------------
                // LOAD EMPLOYEE TRAINS
                // -----------------------------

                await loadEmployeeTrains();


            } catch (error) {

                console.error(
                    "Employee login error:",
                    error
                );


                message.textContent =
                    "Unable to connect to TrackX backend.";
            }

        }
    );
}


// =========================================
// EMPLOYEE TRAIN DASHBOARD
// =========================================

async function loadEmployeeTrains() {

    const availableList =
        document.getElementById(
            "availableTrainList"
        );

    const unavailableList =
        document.getElementById(
            "unavailableTrainList"
        );


    if (
        !availableList ||
        !unavailableList
    ) {
        console.warn(
            "Employee train lists not found."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/trains`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load trains"
            );
        }


        const data =
            await response.json();


        availableList.innerHTML = "";

        unavailableList.innerHTML = "";


        // -----------------------------
        // SEPARATE TRAINS
        // -----------------------------

        const availableTrains =
            data.trains.filter(
                train =>
                    Number(train.available) === 1
            );


        const unavailableTrains =
            data.trains.filter(
                train =>
                    Number(train.available) === 0
            );


        // =========================================
        // AVAILABLE TRAINS
        // =========================================

        if (
            availableTrains.length === 0
        ) {

            availableList.innerHTML = `
                <p class="empty-train-message">
                    No trains available.
                </p>
            `;

        } else {

            availableTrains.forEach(
                train => {

                    availableList.appendChild(
                        createEmployeeTrainRow(
                            train,
                            true
                        )
                    );

                }
            );
        }


        // =========================================
        // UNAVAILABLE TRAINS
        // =========================================

        if (
            unavailableTrains.length === 0
        ) {

            unavailableList.innerHTML = `
                <p class="empty-train-message">
                    All trains are currently available.
                </p>
            `;

        } else {

            unavailableTrains.forEach(
                train => {

                    unavailableList.appendChild(
                        createEmployeeTrainRow(
                            train,
                            false
                        )
                    );

                }
            );
        }


    } catch (error) {

        console.error(
            "Employee train loading error:",
            error
        );


        availableList.innerHTML =
            "<p>Unable to load trains.</p>";


        unavailableList.innerHTML =
            "<p>Unable to load trains.</p>";
    }
}


// =========================================
// CREATE EMPLOYEE TRAIN ROW
// =========================================

function createEmployeeTrainRow(
    train,
    isAvailable
) {

    const row =
        document.createElement("div");


    row.className =
        "employee-train-row";


    const status =
        isAvailable
            ? "AVAILABLE"
            : "NOT AVAILABLE";


    const statusClass =
        isAvailable
            ? "available"
            : "unavailable";


    const newStatus =
        !isAvailable;


    const buttonText =
        isAvailable
            ? "MARK NOT AVAILABLE"
            : "MARK AVAILABLE";


    row.innerHTML = `

        <div class="employee-train-info">

            <strong>
                ${train.name}
            </strong>

            <span>
                Capacity: ${train.capacity}
            </span>

        </div>


        <div class="employee-status ${statusClass}">
            ${status}
        </div>


        <button
            type="button"
            class="status-button"
        >
            ${buttonText}
        </button>

    `;


    const button =
        row.querySelector(
            ".status-button"
        );


    if (button) {

        button.addEventListener(
            "click",
            () => {

                changeTrainStatus(
                    train.id,
                    newStatus
                );

            }
        );
    }


    return row;
}


// =========================================
// CHANGE TRAIN AVAILABILITY
// =========================================

async function changeTrainStatus(
    trainId,
    newStatus
) {

    const token =
        localStorage.getItem(
            "trackx_employee_token"
        );


    if (!token) {

        alert(
            "Employee session expired. Please login again."
        );

        return;
    }


    console.log(
        "Changing train:",
        trainId,
        "New status:",
        newStatus
    );


    try {

        const response =
            await fetch(
                `${API_URL}/employee/trains/${trainId}/status`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`
                    },

                    body: JSON.stringify({
                        available:
                            newStatus
                    })
                }
            );


        const data =
            await response.json();


        console.log(
            "Status response:",
            data
        );


        if (!response.ok) {

            alert(
                data.detail ||
                "Unable to change train status."
            );

            return;
        }


        console.log(
            "Train status updated successfully."
        );


        // Reload both columns
        await loadEmployeeTrains();


    } catch (error) {

        console.error(
            "Train status error:",
            error
        );


        alert(
            "Unable to connect to TrackX backend."
        );
    }
}


// =========================================
// EMPLOYEE LOGOUT
// =========================================

const employeeLogoutButton =
    document.getElementById(
        "employeeLogoutButton"
    );


if (employeeLogoutButton) {

    employeeLogoutButton.addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "trackx_employee_token"
            );


            const dashboard =
                document.getElementById(
                    "employeeDashboard"
                );


            const loginBox =
                document.getElementById(
                    "employeeLogin"
                );


            if (dashboard) {

                dashboard.style.display =
                    "none";
            }


            if (loginBox) {

                loginBox.style.display =
                    "block";
            }


            const username =
                document.getElementById(
                    "employeeUsername"
                );


            const password =
                document.getElementById(
                    "employeePassword"
                );


            const message =
                document.getElementById(
                    "loginMessage"
                );


            if (username) {
                username.value = "";
            }


            if (password) {
                password.value = "";
            }


            if (message) {
                message.textContent = "";
            }

        }
    );
}


// =========================================
// LOAD ML GENERATED SCHEDULE
// =========================================

async function loadMLSchedule() {

    const scheduleList =
        document.getElementById(
            "scheduleList"
        );


    if (!scheduleList) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/schedule`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load schedule"
            );
        }


        const data =
            await response.json();


        scheduleList.innerHTML = "";


        if (
            !data.schedule ||
            data.schedule.length === 0
        ) {

            scheduleList.innerHTML = `
                <p class="no-trains">
                    No AI schedule available.
                </p>
            `;

            return;
        }


        data.schedule.forEach(item => {

            const row =
                document.createElement("div");


            row.className =
                "schedule-row";


            row.innerHTML = `

                <div class="schedule-time">
                    ${item.time}
                </div>


                <div class="schedule-route">

                    <strong>
                        ${item.from_station}
                        →
                        ${item.to_station}
                    </strong>

                </div>


                <div class="schedule-demand">

                    Demand:
                    ${item.predicted_demand}

                </div>


                <div class="schedule-trains">

                    ${item.trains_required}
                    Train

                </div>

            `;


            scheduleList.appendChild(row);

        });


    } catch (error) {

        console.error(
            "ML schedule loading error:",
            error
        );


        scheduleList.innerHTML = `
            <p class="no-trains">
                Unable to load AI schedule.
            </p>
        `;
    }
}


loadMLSchedule();


// =========================================
// END OF TRACKX SCRIPT
// =========================================