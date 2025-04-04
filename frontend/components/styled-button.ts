class StyledButton extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });

        // Create button element
        const button = document.createElement('button');
        button.textContent = this.getAttribute('label') || 'Click Me';

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            button {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
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