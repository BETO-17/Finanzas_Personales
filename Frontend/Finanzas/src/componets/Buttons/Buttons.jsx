import './Buttons.css'

export function Buttons({ name, id }) {
    return (
        <button id={id}>{name}</button>
    )
}