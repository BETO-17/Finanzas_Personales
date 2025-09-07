
import './App.css'
import { ReturnInputs } from './componets/inputs/input'
import { Buttons } from './componets/Buttons/Buttons'
import { ReturnTable } from './componets/Table/Table'

function App() {


  //renderisado html
  return (
    <>
      <header>
        <h1 className='Title'>Crud Transaccion</h1>
      </header>
      <form>
        <section>
          <div className='Inputs'>

            <ReturnInputs name={"Categoria"} />
            <ReturnInputs name={"Nombres"} />
            <ReturnInputs name={"Fecha"} />
            <ReturnInputs name={"Monto"} />
            <ReturnInputs name={"Tipo_de_Transaccion"} />
            <ReturnInputs name={"Destinatario"} />
          </div>
          <div>
            <Buttons id={"Registrar"} name={"Registrar"} />
            <Buttons id={"Limpiar"} name={"Limpiar"} />
          </div>

        </section>
        <section>
          <ReturnTable />
        </section>

      </form>
    </>
  )
}

export default App
