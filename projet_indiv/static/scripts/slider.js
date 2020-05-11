var slider = document.getElementById('range');


noUiSlider.create(slider, {
    start: [ 0, 100], // Handle start position
    step: 1, // Slider moves in increments of '10'
    margin: 1, // Handles must be more than '20' apart
    connect: true, // Display a colored bar between the handles
    behaviour: 'tap-drag', // Move handle on tap, bar is draggable
    tooltips: [true, true], //to see the values
    range: { // Slider can select '0' to '100'
        'min': 0,
        'max': 100
    },
});

var minProgressInput = document.getElementById('minProgress'),
    maxProgressInput = document.getElementById('maxProgress');

// When the slider value changes, update the input and span
slider.noUiSlider.on('update', function( values, handle ) {
    if ( handle ) {
        maxProgressInput.value = values[handle];
    } else {
        minProgressInput.value = values[handle];
    }
});

minProgressInput.addEventListener('change', function(){
    slider.noUiSlider.set([null, this.value]);
});

maxProgressInput.addEventListener('change', function(){
    slider.noUiSlider.set([null, this.value]);
});


// var slider = document.getElementById('progress');
//
//
// noUiSlider.create(slider, {
//     start: [0, 100],
//     connect: true,
//     tooltips: [true, true],
//     range: {
//         'min': 0,
//         'max': 100
//     }
// });
//
// $("#sliderRange").val(slider.get());
//
// slider.on("change", function() {
//   console.log("here")
//   $("#sliderRange").val(slider.get());
// });


//////////////



// var select = document.getElementById('min_progress');
//
// // Append the option elements
// for (var i = -20; i <= 40; i++) {
//
//     var option = document.createElement("option");
//     option.text = i;
//     option.value = i;
//
//     select.appendChild(option);
// }
// var html5Slider = document.getElementById('progress');
//
// noUiSlider.create(html5Slider, {
//     start: [10, 30],
//     connect: true,
//     range: {
//         'min': 0,
//         'max': 100
//     }
// });
// var inputNumber = document.getElementById('max_progress');
// //
// html5Slider.noUiSlider.on('update', function (values, handle) {
//
//     var value = values[handle];
//
//     if (handle) {
//         inputNumber.value = value;
//     } else {
//         select.value = Math.round(value);
//     }
// });
//
// select.addEventListener('change', function () {
//     html5Slider.noUiSlider.set([this.value, null]);
// });
//
// inputNumber.addEventListener('change', function () {
//     html5Slider.noUiSlider.set([null, this.value]);
// });
