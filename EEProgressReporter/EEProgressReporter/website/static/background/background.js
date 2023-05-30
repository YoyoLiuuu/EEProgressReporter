'use strict'

const outputColor = document.querySelector(".output-color");
/** @type {HTMLInputElement} */
const outputCode = document.querySelector(".output-code");
// ⚠️ Removed `hexString`, we don't need it.

/** Generates a random hex value between `00` and `ff` */
const randomHex = () =>
  Math.floor(Math.random() * 256)
    .toString(16)
    .padStart(2, "0");

/** Uses `randomHex` to generate a random color string */
const randomColor = () => `#${[...Array(3)].map(randomHex).join("")}`;

/** Returns a random value between 0 and 360 */
const randomAngle = () => `${Math.floor(Math.random() * 361)}deg`;

/** Generate random linear gradient values */
const randomGradient = () => [randomAngle(), randomColor(), randomColor()];

/** Update UI with new values */
const update = () => {
  const [angle, color1, color2] = randomGradient();
  // use custom properties instead of CSS directly.
  outputColor.style.setProperty("--color-1", randomColor());
  outputColor.style.setProperty("--color-2", randomColor());
  outputColor.style.setProperty("--angle", randomAngle());
  outputCode.value = `background: linear-gradient(${angle}, ${color1}, ${color2});`;
};

update()



