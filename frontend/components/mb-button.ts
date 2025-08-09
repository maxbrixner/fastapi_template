const TEMPLATE = `
<style>
    :host {
        display: inline-block;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        --button-color: #ffffff;
        --button-background: #007bff;
        --button-hover-background: #0056b3;
        --button-active-background: #004085;
        --button-border-color: var(--button-background);
        --button-border-radius: 0.25rem;
        --button-padding: 0.5rem 1rem;
        --button-font-size: 1rem;
        --button-font-weight: 600;
        --button-box-shadow: none;
        --button-transition: all 0.2s ease;
    }

    button {
        all: unset;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        cursor: pointer;
        border: 1px solid var(--button-border-color);
        border-radius: var(--button-border-radius);
        padding: var(--button-padding);
        font-size: var(--button-font-size);
        font-weight: var(--button-font-weight);
        color: var(--button-color);
        background-color: var(--button-background);
        box-shadow: var(--button-box-shadow);
        transition: var(--button-transition);
        user-select: none;
    }

    button:hover {
        background-color: var(--button-hover-background);
        border-color: var(--button-hover-background);
    }

    button:active {
        background-color: var(--button-active-background);
        border-color: var(--button-active-background);
        transform: translateY(1px);
    }

    :host([disabled]) button {
        cursor: not-allowed;
        opacity: 0.6;
        background-color: var(--button-background);
        border-color: var(--button-background);
        transform: none;
    }

    :host([variant="outline"]) button {
        --button-color: var(--button-background);
        --button-background: transparent;
        --button-hover-background: rgba(0, 123, 255, 0.1);
        --button-border-color: var(--button-background);
    }

    :host([variant="ghost"]) button {
        --button-background: transparent;
        --button-hover-background: rgba(0, 0, 0, 0.05);
        --button-border-color: transparent;
        --button-color: #212529;
    }
</style>
<button>
    <slot></slot>
</button>
`

class MbButton extends HTMLElement {
    protected _button: HTMLButtonElement;

    static get observedAttributes(): string[] {
        return ['disabled', 'type', 'variant'];
    }

    constructor() {
        super();

        const shadowRoot = this.attachShadow({ mode: 'open' });

        const template = document.createElement('template');
        template.innerHTML = TEMPLATE;

        const templateContent = template.content.cloneNode(true);
        shadowRoot.appendChild(templateContent);

        this._button = shadowRoot.querySelector('button') as HTMLButtonElement;
    }

    connectedCallback(): void {
        this.updateAttributes();
        this._button.addEventListener('click', this.onClick.bind(this));
    }

    disconnectedCallback(): void {
        this._button.removeEventListener('click', this.onClick.bind(this));
    }

    attributeChangedCallback(name: string, oldValue: string | null, newValue: string | null): void {
        console.log(`Attribute changed: ${name}, Old Value: ${oldValue}, New Value: ${newValue}`);
        if (oldValue !== newValue) {
            this.updateAttributes();
        }
    }

    private updateAttributes(): void {
        if (this.hasAttribute('disabled')) {
            this._button.setAttribute('disabled', '');
            this._button.setAttribute('aria-disabled', 'true');
        } else {
            this._button.removeAttribute('disabled');
            this._button.removeAttribute('aria-disabled');
        }

        if (this.hasAttribute('type')) {
            this._button.setAttribute('type', this.getAttribute('type') || 'button');
        } else {
            this._button.removeAttribute('type');
        }
    }

    get disabled(): boolean {
        return this.hasAttribute('disabled');
    }

    set disabled(value: boolean) {
        if (value) {
            this.setAttribute('disabled', '');
        } else {
            this.removeAttribute('disabled');
        }
    }

    protected onClick(event: Event) {
        if (this.disabled) {
            event.preventDefault();
            event.stopImmediatePropagation();
        } else {
            this.dispatchEvent(new Event('click', { bubbles: true, composed: true }));
        }
    }
}

customElements.define('mb-button', MbButton);