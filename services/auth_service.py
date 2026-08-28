from sqlalchemy.orm import Session
from database.models import User

from utils.security import(
    hash_password,
    verify_password,
    create_access_token
)

class AuthService:
    """
    it is used for authentication process 
    """
    @staticmethod
    def register_user(
        db:Session,
        full_name: str,
        email: str,
        password: str
    ) -> User:

        """
        this part is used to check whether the email id is already existing
        """
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            raise ValueError(
                "User with this email already exists."
            )
        
        """
        this part is used to hash the password before storing it
        """
        hashed_password = hash_password(password)

        """
        this part is used for creating the new user
        """
        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password
        )

        #add the new user to the database
        db.add(user)

        #save the changes in the db
        db.commit()

        #store the values in the db and refresh the objects with the database generated values
        db.refresh(user)

        return user

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str
    ) -> dict:

        #identifing the user through email
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        ) 
        #it shows the information like the user doesnot exists
        if not user:
            raise ValueError(
                "Invalid email or password."
            )

        #it is used to verify whether the password is crt or not
        password_valid = verify_password(
            password,
            user.hashed_password
        )

        if not password_valid:
            raise ValueError(
                "Invalid email or password."
            )

        #this creates the JWT access tokens for the user stores in the database
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        return{
            "access_token": access_token,
            "token_type": "bearer"
        }
