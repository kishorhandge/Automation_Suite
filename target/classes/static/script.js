function streamConsole(url, consoleId, statusId)
{
    var consoleBox = document.getElementById(consoleId);
    var status = document.getElementById(statusId);

    consoleBox.innerHTML = "";
    status.innerText = "Running";

    var eventSource = new EventSource(url);

    eventSource.onmessage = function(event)
    {
        consoleBox.innerHTML = consoleBox.innerHTML + event.data + "<br>";
        consoleBox.scrollTop = consoleBox.scrollHeight;
    };

    eventSource.onerror = function()
    {
        status.innerText = "Stopped";
        eventSource.close();
    };
}



/////////////////////////////////////////////////
// Disk Sanitizer
/////////////////////////////////////////////////

function startDuplicate()
{
    var path = document.getElementById("dupPath").value.trim();

    if(path == "")
    {
        alert("Please enter directory path");
        return;
    }

    if(path.length < 3)
    {
        alert("Path looks invalid");
        return;
    }

    streamConsole(
        "/api/duplicate?path=" + encodeURIComponent(path),
        "dupConsole",
        "dupStatus"
    );
}

function stopDuplicate()
{
    fetch("/api/stop/duplicate",{method:"POST"});
    document.getElementById("dupStatus").innerText = "Stopped";
}



/////////////////////////////////////////////////
// Backup Automation
/////////////////////////////////////////////////

function startBackup()
{
    var interval = document.getElementById("backupInterval").value.trim();
    var source = document.getElementById("backupSource").value.trim();

    if(interval == "" || source == "")
    {
        alert("Please fill all fields");
        return;
    }

    if(isNaN(interval))
    {
        alert("Interval must be numeric");
        return;
    }

    if(interval <= 0)
    {
        alert("Interval must be greater than zero");
        return;
    }

    streamConsole(
        "/api/backup?interval=" + interval + "&source=" + encodeURIComponent(source),
        "backupConsole",
        "backupStatus"
    );
}

function stopBackup()
{
    fetch("/api/stop/backup",{method:"POST"});
    document.getElementById("backupStatus").innerText = "Stopped";
}



/////////////////////////////////////////////////
// Process Surveillance
/////////////////////////////////////////////////

function startMonitor()
{
    var interval = document.getElementById("monInterval").value.trim();
    var folder = document.getElementById("monFolder").value.trim();

    if(interval == "" || folder == "")
    {
        alert("Please fill all fields");
        return;
    }

    if(isNaN(interval))
    {
        alert("Interval must be numeric");
        return;
    }

    if(interval <= 0)
    {
        alert("Interval must be greater than zero");
        return;
    }

    streamConsole(
        "/api/monitor?interval=" + interval + "&folder=" + encodeURIComponent(folder),
        "monConsole",
        "monStatus"
    );
}

function stopMonitor()
{
    fetch("/api/stop/monitor",{method:"POST"});
    document.getElementById("monStatus").innerText = "Stopped";
}



/////////////////////////////////////////////////
// Temporary File Cleaner
/////////////////////////////////////////////////

function startTempCleaner()
{
    var path = document.getElementById("tempPath").value.trim();

    if(path == "")
    {
        alert("Please enter directory path");
        return;
    }

    if(path.length < 3)
    {
        alert("Path looks invalid");
        return;
    }

    streamConsole(
        "/api/tempclean?path=" + encodeURIComponent(path),
        "tempConsole",
        "tempStatus"
    );
}

function stopTempCleaner()
{
    fetch("/api/stop/tempclean",{method:"POST"});
    document.getElementById("tempStatus").innerText = "Stopped";
}