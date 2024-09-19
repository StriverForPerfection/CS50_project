$("#commit").on("submit", function()
{
    // tag:attribute is used to select tags/elements with this attribute
    var intruders = "";
    var innocents = "";
    $("input:checked[name = 'innocent']").each(function()
    {
        if (intruders === "")
        {
            intruders += $(this).val();
        }
        else
        {
            intruders += ("," + $(this).val());
        }
    })

    $("input:checked[name = 'intruder']").each(function() // Credit for CSS selector: https://stackoverflow.com/questions/12340737/specify-multiple-attribute-selectors-in-css and CoPilot
    {
        if (innocents === "")
        {
            innocents += $(this).val();
        }
        else
        {
            innocents += ("," + $(this).val());
        }
    })

    $("input:checked[name = 'newInnocent']").each(function()
    {
        if (intruders === "")
        {
            intruders += $(this).val();
        }
        else
        {
            intruders += ("," + $(this).val());
        }
    })

    $("input:not(:checked)[name = 'newInnocent']").each(function()
    {
        if (innocents === "")
        {
            innocents += $(this).val();
        }
        else
        {
            innocents += ("," + $(this).val());
        }
    })

    console.log(intruders);
    console.log($("input[id='intruders']").text());

    $("input[id='intruders']").val(intruders);
    console.log($("input[id='intruders']").val());
    console.log("Innocents: ")
    $("input[id = 'innocents']").val(innocents)
    console.log(innocents);
    console.log($("toggleGuardian").val())

    // var newIntruders = "";
    
    // $("#newInnocents").val(newInnocents);
    // $("#newIntruders").val(newIntruders);

    // console.log("1111", $("#newInnocents").val())
    // console.log("2222", $("#newIntruders").val())


})



function sleep(ms) // Function to add a delay between icon changes
{
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function wait(time) 
{
    // A higher value would be slow, and a lower one will be too quick for the browser such that it will stagger.
    await sleep(time);
};
// Credits: https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep

// the function inside ".on" shall be made async, and wait shall be preceeded by await for the sleep function to
// work, where a while loop doesn't wait for asynchronous functions to execute, except if we do this. BingCopilot.

async function warn()
{
    let i = 1;

    while(i < 20)
    {
        console.log("Hello!");

        $("#favi").attr("href", "static/alert1.ico");
        // $("title").html("Intruder!"); // Painful for one's eyes.
        await wait(250);

        $("#favi").attr("href", "static/alert2.ico");
        // $("title").html("Thief!");
        await wait(250);
        i += 1;
    }

};

$("#alrtbtn").on("click", async function ()
{
    console.log($("#toggleGuardian").val())
    console.log("warning");
    // await wait(120000);
})
// $("#toggleGuardian").on("change", async function ()
// {

var cage = $("table[id = 'newIntruders']");

function createRow(intruder)
{
    var tmp = $("<tr style = 'position: relative'></tr>"); // Create a new tr tag, of attributes:...
    var cell = $("<td style = 'margin: 6px'></td>").text(intruder);
    var tmpspan = $("<span style = 'display: inline-block; position: absolute; left: 400px; padding: 4px'></span>");
    var check = $("<input>", {type : "checkbox", value: intruder, name: "newInnocent", class : 'form-check-input', style: 'margin: 6px; padding: 3px'});

    tmpspan.append(check);
    cell.append(tmpspan);
    tmp.append(cell);
    cage.append(tmp);
    
    console.log(intruder);
}
var newIntruders = ["a", "b", "c"];

function getIntruders()
{
    
    // Credit: https://github.com/hankhank10/axios-example and Bing Copilot
    if ($("#toggleGuardian").val() == "1")
    {
        console.log("count zero!");

        (async () =>
        {
            console.log("count half!");

            try
            {
                const response = await fetch("/detectIntruders");
                const data = await response.json();
                console.log("data: ", data);
                cage.empty();
                console.log("count one!");
                for (let intruder of data)
                {
                    console.log("count me!");
                    // newIntruders.push(intruder)
                    createRow(intruder);
                }

                // createRow(newIntruders[0]);
                if (data.length > 0)
                {
                    warn();
                }
            }  
            catch(error)
            {
                console.error("Error in fetching intruders: ", error);
            }
        })()           
    }
}

getIntruders()
var repeat = window.setInterval(getIntruders, 120000)
    

