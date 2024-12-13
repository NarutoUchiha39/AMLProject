import { Route,Routes } from "react-router"
import Login from "./components/login/Login"
import Resgister from "./components/register/Resgister"
import Navbar from "./components/navbar/Navbar"
import Home from "./components/Home/Home"
function App() {
  return (
    <>
      <Routes>
        <Route element={<Navbar/>}>
          <Route element={<Login/>} path="/login" />
          <Route element={<Resgister/>} path="/register" />
          <Route element={<Home/>} path="/" />
        </Route>
      </Routes>
    </>
  )
}

export default App
