import React from 'react';
import moment from 'moment';
import ReactMarkdown from 'react-markdown'
import { Buffer } from 'buffer';
import './Message.css';

export default function Message(props) {
    const {
        data,
        author,
        showTimestamp,
    } = props;

    const friendlyTimestamp = moment(data.timestamp).format('LLLL');
    return (
        <div className={[
            'message',
            `${data.author === author ? 'mine' : ''}`,
        ].join(' ')}>
            {   showTimestamp &&
                <div className="timestamp">
                    {friendlyTimestamp}
                </div>
            }

            <div className="bubble-container">
                <div className="bubble" title={friendlyTimestamp}>
                    <ReactMarkdown>
                        {Buffer.from(data.message, 'base64').toString()}
                    </ReactMarkdown>
                </div>
            </div>
        </div>
    );
}