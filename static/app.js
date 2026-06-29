/* Input Search From Focus-In/Out */
$(".inputForm").focusin(function(){
	$(this).prev("label").addClass("inputLabel-focusIn");
});

// Input Search From Focus-Out */
$(".inputForm").focusout(function(){
	var inputForm = $(this).val();

	if (inputForm.length > 0) {
		$(this).prev("label").addClass("inputLabel-focusIn");
	} else {
		$(this).prev("label").removeClass("inputLabel-focusIn");
	}
});

/* Input Onward/Reture Date Focus-In/Out */
$("#input-label-onward-date, #input-label-return-date").focusin(function(){
	$(this).attr("type", "date");
});

// Input Onward/Reture Date Focus-Out */
$("#input-label-onward-date, #input-label-return-date").focusout(function(){
	var inputFormDate = $(this).val();

	if (inputFormDate.length > 0) {
		$(this).attr("type", "date");
	} else {
		$(this).attr("type", "text");
	}
});

/* Pass Input-From's Locations to Input field */
// From Locations Data
var inputFromList = [
	{ fromLocation : "Mumbai"},
	{ fromLocation : "Alibaug"},
	{ fromLocation : "Sindhudurg"},
];

var optionFrom;
var inputFromDatalist = $("#input-from-list");

for (var i = 0; i < inputFromList.length; i++) {
	optionFrom = $("<option></option>");
	optionFrom.attr("value", inputFromList[i].fromLocation);
	inputFromDatalist.append(optionFrom);
}

/* Pass Input-To's Locations to Input field */
// To Locations Data
var inputToList = [
	{ toLocation : "Alibaug"},
	{ toLocation : "Mumbai"},
	{ toLocation : "Sindudurg"}
];

var optionTo;
var inputToDatalist = $("#input-to-list");

for (var i = 0; i < inputToList.length; i++) {
	optionTo = $("<option></option>");
	optionTo.attr("value", inputToList[i].toLocation);
	inputToDatalist.append(optionTo);
}

// Data Filter
$("#input-label-from").change(function(){
	var dataSelect = $(this).val();
	console.log(dataSelect);

	$("#input-to-list").find("option[value='"+dataSelect+"']").remove();
});





var getHubergerIcon = document.getElementById("hamburger-menu");
    var getHubergerCrossIcon = document.getElementById("hamburger-cross");
    var getMobileMenu = document.getElementById("mobile-menu");

    getHubergerIcon.addEventListener("click", function () {
        console.log("hello");
        getMobileMenu.style.display = "flex";
        setTimeout(function () {
            getMobileMenu.style.transform = "translateX(0%)"; // Slide in the menu
        }, 50); // Add a small delay for better transition effect
    });

    getHubergerCrossIcon.addEventListener("click", function () {
        console.log("hello");
        getMobileMenu.style.transform = "translateX(-100%)"; // Slide out the menu
        setTimeout(function () {
            getMobileMenu.style.display = "none";
        }, 300); // Wait for the transition to end before hiding
    });

    // Check if screen size changes to desktop view and hide mobile menu
    window.addEventListener("resize", function () {
        if (window.innerWidth > 770) {
            getMobileMenu.style.display = "none";
        }
    });


	//when we select one way option return date field disable

	
	document.addEventListener("DOMContentLoaded", function () {
		const returnDateInput = document.getElementById("input-label-return-date");

		// Hide return date input initially
		returnDateInput.style.display = "none";

		// Get the radio buttons
		const oneWayOption = document.getElementById("option1");
		const returnOption = document.getElementById("option2");

		// Add event listeners to radio buttons
		oneWayOption.addEventListener("click", function () {
			// Hide return date input when one way option is selected
			returnDateInput.style.display = "none";
		});

		returnOption.addEventListener("click", function () {
			// Show return date input when return option is selected
			returnDateInput.style.display = "block";
		});
	});




	//when user login then redirect to home page and disable sign in button and shows a user profile
	document.addEventListener("DOMContentLoaded", function () {
		const signinButton = document.getElementById("signin-button");
		const profileDropdown = document.getElementById("profile-dropdown");

		// Mock login function
		function login() {
			// Simulate successful login
			signinButton.classList.add("hidden");
			profileDropdown.classList.remove("hidden");
		}

		signinButton.addEventListener("click", function (event) {
			event.preventDefault();
			login();
		});
	});

	function toggle() {
		document.querySelector(".profile-dropdown-list").classList.toggle("active");
	}