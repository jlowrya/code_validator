import { Component } from 'react'
import axios from 'axios';

class ValidatorForm extends Component {
    constructor(props) {
      super(props);
      this.state = {
          phone: '',
          code: '',
          codeCreated: false,
          message: 'Provide a phone number to send verification code to.'
      };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.verifyCode = this.verifyCode.bind(this);
    }
  
    handleChange(event) {
        const target = event.target;
        const value =  target.value;
        const name = target.name;

        console.log(target)

        this.setState({
            [name]: value
        });
    }
  
    handleSubmit(event) {
        console.log('Handling submit')
        const client = axios.create({
            baseURL: 'https://0245u3tfo7.execute-api.us-east-1.amazonaws.com/dev/codes'
          })
        console.log('Created client')
        client.post(
            `?phone=${this.state.phone}`
        ).then((resp) => {
            console.log(resp.data)
            this.setState({
                ...this.state,
                message: `A verification code has been sent to ${this.state.phone}`,
                codeCreated: true
            })
        }).catch((e) => {
            console.log(e)
        })
        event.preventDefault();
    }

    verifyCode(event) {
        console.log(`Verifying code ${this.state.code} for ${this.state.phone}`)
        console.log('Handling submit')
        const client = axios.create({
            baseURL: 'https://0245u3tfo7.execute-api.us-east-1.amazonaws.com/dev/codes'
        })
        console.log('Created client')
        client.get(
            `?phone=${this.state.phone}&code=${this.state.code}`
        ).then((resp) => {
            console.log(resp.data)
            this.setState({
                message: `Code successfully validated!`
            })
        }).catch((e) => {
            console.log(e)
            this.setState({
                message: `Code validation failed.`
            })
        })
        event.preventDefault();
    }
  
    render() {
      return (
          <div>
            {
                 this.state.codeCreated ? 
             <form onSubmit={this.verifyCode}>
                 <label>
                 Verification code:
                 <input type="text" value={this.state.code} name='code' onChange={this.handleChange} />
             </label>
             <br/>
             <input type="submit" value="Verify" />
             </form> 
             :
             <form onSubmit={this.handleSubmit}>
                 <label>
                 Phone number:
                 <input type="text" value={this.state.phone} name='phone' onChange={this.handleChange} />
             </label>
             <br/>
             <input type="submit" value="Submit" />
             </form> 
            }
            <p>{this.state.message}</p>
          </div> 
      );
    }
  }

  export default ValidatorForm;