import React, { useState } from 'react';

function MyComponent() {
    const [showImage, setShowImage] = useState(false);
    const [versionInfo, setVersionInfo] = useState(false);

    const handleTutorialClick = () => {
        setShowImage(true);
        setVersionInfo(false);
    };

    const handleAboutClick = () => {
        setShowImage(false);
        setVersionInfo(true);
    };

    return (
        <div>
            <nav>
                <ul>
                    <li onClick={handleTutorialClick}>教程</li>
                    <li onClick={handleAboutClick}>关于</li>
                </ul>
            </nav>
            {showImage && (
                <div>
                    <img src="https://via.placeholder.com/150" alt="操作示意图" />
                </div>
            )}
            {versionInfo && <p>当前版本: 1.0.0</p>}
        </div>
    );
}

export default MyComponent; 