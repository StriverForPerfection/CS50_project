$("#commit").on("submit", function()
{
    // tag:attribute is used to select tags/elements with this attribute
    var intruders = "";
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
    console.log(intruders);
    console.log($("input[id='intruders']").text());

    $("input[id='intruders']").val(intruders);
    console.log($("input[id='intruders']").val());

    var innocents = "";
    $("input:checked[name = 'intruder']").each(function()
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
    console.log(innocents);
    console.log($("input[id='innocents']").text());

    $("input[id='innocents']").val(innocents);
    console.log($("input[id='innocents']").val());
})