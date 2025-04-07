"use strict";
class StyledButton extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        // Create button element
        const button = document.createElement('button');
        //button.textContent = this.getAttribute('label') || 'Click Me';
        button.innerHTML = `<slot></slot>`; // Use a slot for the button's content
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            button {
                background-color: var(--background);
                color: var(--color-gray-900);
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                font-family: var(--font-sans);

            }
            button:hover {
                background-color: #0056b3;
            }
        `;
        // Append elements to shadow DOM
        shadow.appendChild(style);
        shadow.appendChild(button);
    }
}
// Define the custom element
if (!customElements.get('styled-button')) {
    customElements.define('styled-button', StyledButton);
}
class StyledDialog extends HTMLElement {
    constructor() {
        var _a;
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        // Create dialog container
        this._dialog = document.createElement('div');
        this._dialog.classList.add('dialog');
        this._dialog.innerHTML = `
            <div class="dialog-content">
                <slot name="content">Default Dialog Content</slot>
                <button class="close-button">Close</button>
            </div>
        `;
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .dialog {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                display: none;
                justify-content: center;
                align-items: center;
            }
            .dialog-content {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .close-button {
                margin-top: 10px;
                padding: 8px 16px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .close-button:hover {
                background-color: #0056b3;
            }
        `;
        // Append elements to shadow DOM
        shadow.appendChild(style);
        shadow.appendChild(this._dialog);
        // Add event listener for the close button
        (_a = this._dialog.querySelector('.close-button')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', () => this.close());
    }
    open() {
        this._dialog.style.display = 'flex';
    }
    close() {
        this._dialog.style.display = 'none';
    }
}
// Define the custom element
if (!customElements.get('styled-dialog')) {
    customElements.define('styled-dialog', StyledDialog);
}
