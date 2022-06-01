import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';

export default function Login() {
    const [roomNameValue, setRoomNameValue] = React.useState('');
    const [userNameValue, setUserNameValue] = React.useState('');

    const handleRoomNameChange = (event) => {
        setRoomNameValue(event.target.value);
    };

    const handleUserNameChange = (event) => {
        setUserNameValue(event.target.value);
    };

    const connectToRoom = () => {
        if (roomNameValue.trim() === '' || userNameValue.trim() === '')
            return
        localStorage.setItem('author', userNameValue.trim())
        window.location.href = `chat/${roomNameValue}`
    }

    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
            className="login-box"
        >
            <div>
                <TextField
                    required
                    id="outlined-required"
                    label="Nick"
                    value={userNameValue}
                    onChange={handleUserNameChange}

                />
            </div>
            <div>
                <TextField
                    id="standard-multiline-static"
                    label="Room name"
                    multiline
                    required
                    rows={4}
                    variant="outlined"
                    value={roomNameValue}
                    onChange={handleRoomNameChange}
                />
            </div>
            <Button className='submit-button' variant="contained" onClick={connectToRoom}>Contained</Button>
        </Box>
    );
}
