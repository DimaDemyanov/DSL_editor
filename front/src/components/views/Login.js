import React from 'react';
import { useState } from "react";
import { Link, useHistory} from "react-router-dom";
import Form from '../../utilities/Forms'

const SERVER_URL = process.env.REACT_APP_SERVER_URL
const LOGIN_URL = SERVER_URL + '/login'


const Login = () => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [remember, setRemember] = useState(false);
    const [validate, setValidate] = useState({});
    const [showPassword, setShowPassword] = useState(false);

    const history = useHistory();

    const validateLogin = () => {
        let isValid = true;

        let validator = Form.validator({
            username: {
                value: username,
                isRequired: true,
                minLength: 6
            },
            password: {
                value: password,
                isRequired: true,
                minLength: 6
            }
        });

        if (validator !== null) {
            setValidate({
                validate: validator.errors
            })

            isValid = false
        }
        return isValid;
    }

    const authenticate = async (e) => {
        e.preventDefault();

        const validate = validateLogin();
        

        if (validate) {
            let request = await fetch(LOGIN_URL, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json   '
                },
                body: JSON.stringify({
                  "username": username
                })
              });
            
            let response = await request.json()

            console.log(response)
            if (request.status != 200) {
                alert('Unable to login');
            } else {
                console.log('DIMA ' + response)
                document.cookie = 'username=' + response.username
                setValidate({});
                setUsername('');
                setPassword('');
                history.push('/editor')
            }
        }
    }

    const togglePassword = (e) => {
        if (showPassword) {
            setShowPassword(false);
        } else {
            setShowPassword(true)
        }
    }

    return (
        <div className="row g-0 auth-wrapper">
            <div className="col-12 col-md-5 col-lg-6 h-100 auth-background-col">
                <div className="auth-background-holder"></div>
                <div className="auth-background-mask"></div>
            </div>

            <div className="col-12 col-md-7 col-lg-6 auth-main-col text-center">
                <div className="d-flex flex-column align-content-end">
                    <div className="auth-body mx-auto">
                        <p>Login to your account</p>
                        <div className="auth-form-container text-start">
                            <form className="auth-form" method="POST" onSubmit={authenticate} autoComplete={'off'}>
                                <div className="username mb-3">
                                    <input type="username"
                                        className={`form-control ${validate.validate && validate.validate.username ? 'is-invalid ' : ''}`}
                                        id="username"
                                        name="username"
                                        value={username}
                                        placeholder="username"
                                        onChange={(e) => setUsername(e.target.value)}
                                    />

                                    <div className={`invalid-feedback text-start ${(validate.validate && validate.validate.username) ? 'd-block' : 'd-none'}`} >
                                        {(validate.validate && validate.validate.username) ? validate.validate.username[0] : ''}
                                    </div>
                                </div>

                                <div className="password mb-3">
                                    <div className="input-group">
                                        <input type={showPassword ? 'text' : 'password'}
                                            className={`form-control ${validate.validate && validate.validate.password ? 'is-invalid ' : ''}`}
                                            name="password"
                                            id="password"
                                            value={password}
                                            placeholder="Password"
                                            onChange={(e) => setPassword(e.target.value)}
                                        />

                                        <button type="button" className="btn btn-outline-primary btn-sm" onClick={(e) => togglePassword(e)} ><i className={showPassword ? 'far fa-eye' : 'far fa-eye-slash'} ></i> </button>

                                        <div className={`invalid-feedback text-start ${(validate.validate && validate.validate.password) ? 'd-block' : 'd-none'}`} >
                                            {(validate.validate && validate.validate.password) ? validate.validate.password[0] : ''}
                                        </div>
                                    </div>


                                    <div className="extra mt-3 row justify-content-between">
                                        <div className="col-6">
                                            <div className="form-check">
                                                <input className="form-check-input" type="checkbox" id="remember" checked={remember} onChange={(e) => setRemember(e.currentTarget.checked)} />
                                                <label className="form-check-label" htmlFor="remember">
                                                    Remember me
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="text-center">
                                    <button type="submit" className="btn btn-primary w-100 theme-btn mx-auto">Log In</button>
                                </div>
                            </form>

                            <hr />
                            <div className="auth-option text-center pt-2">No Account? <Link className="text-link" to="/register" >Sign up </Link></div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
}

export default Login;