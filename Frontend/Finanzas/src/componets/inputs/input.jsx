import './input.css'

export function ReturnInputs({ name }) {
    return (

        <label htmlFor={name}>
            {name}
            <input type="text" id={name} name={name} />
        </label>

    )
}