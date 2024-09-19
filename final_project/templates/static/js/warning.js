function sleep(ms) // Function to add a delay between icon changes
{
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function wait() 
{
    // A higher value would be slow, and a lower one will be too quick for the browser such that it will stagger.
    await sleep(250);
};
// Credits: https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep

// the function inside ".on" shall be made async, and wait shall be preceeded by await for the sleep function to
// work, where a while loop doesn't wait for asynchronous functions to execute, except if we do this. BingCopilot.

$("#reg").on("click", async function()
{
    let i = 1;

    while(i < 500)
    {
        console.log("Hello!");

        $("#favi").attr("href", "static/alert1.ico");
        // $("title").html("Intruder!"); // Painful for one's eyes.
        await wait();

        $("#favi").attr("href", "static/alert2.ico");
        // $("title").html("Thief!");
        await wait();
        i += 1;
    }

});